from rest_framework import serializers
from .models import Visitor, EventWave
from .services.blacklist_service import BlackListService

class VisitorSerializer(serializers.ModelSerializer):
    wave_id = serializers.IntegerField(write_only=True, required=False)



    class Meta:
        model = Visitor
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'vk_link', 'created_at', 'wave_id']
        read_only_fields = ['wave']


    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        middle_name = data.get('middle_name', '')
        
        # Проверка черного списка
        blacklist_service = BlackListService()
        is_blacklisted, reason = blacklist_service.check_blacklist(first_name, last_name, middle_name)
        
        if is_blacklisted:
            raise serializers.ValidationError(f"Посетитель находится в черном списке: {reason}")
        
        return data


    def create(self, validated_data):
        # Извлекаем wave_id и удаляем его из данных
        wave_id = validated_data.pop('wave_id', None)

        # Создаем посетителя
        visitor = Visitor.objects.create(**validated_data)

        # Если указана волна, связываем ее
        if wave_id:
            try:
                wave = EventWave.objects.get(id=wave_id, is_active=True)

                # Проверка capacity
                if wave.current_count >= wave.max_capacity:
                    raise serializers.ValidationError("Достигнуто максимальное количество участников на этой волне")

                visitor.wave = wave
                visitor.save()

                # Увеличение счетчика волны
                wave.current_count += 1
                wave.save()

            except EventWave.DoesNotExist:
                raise serializers.ValidationError("Волна не найдена или неактивна")

        return visitor




class EventWaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWave
        fields = '__all__'
