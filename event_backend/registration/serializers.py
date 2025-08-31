from rest_framework import serializers
from .models import Visitor, EventWave
from .services.blacklist_service import BlackListService



class VisitorSerializer(serializers.ModelSerializer):
    wave_id = serializers.IntegerField(write_only=True, required=False)
    phone = serializers.CharField(max_length=20, required=True)
    telegram = serializers.CharField(required=False, allow_blank=True, max_length=100)
    birth_date = serializers.DateField(
        required=False, 
        allow_null=True # Формат для отображения
    )
    gender = serializers.ChoiceField(
        choices=[('M', 'Мужской'), ('F', 'Женский')],
        required=False,
        allow_blank=True
    )
    university = serializers.CharField(max_length=200, required=True)
    faculty = serializers.CharField(max_length=200, required=True)
    program = serializers.CharField(max_length=200, required=True)
    year = serializers.IntegerField(required=True)
    group = serializers.CharField(max_length=50, required=True)
    transfer = serializers.ChoiceField(
        choices=[('need', 'Нужен'), ('not_need', 'Не нужен')],
        required=True
    )
    health_issues = serializers.CharField(required=False, allow_blank=True)
    allergies = serializers.CharField(required=False, allow_blank=True)


    class Meta:
        model = Visitor
        fields = fields = [
            # Личные данные
            'id', 'first_name', 'last_name', 'middle_name',
            
            # Контактная информация
            'phone', 'vk_link', 'telegram',
            
            # Персональные данные
            'birth_date', 'gender',
            
            # Учебная информация
            'university', 'faculty', 'program', 'year', 'group',
            
            # Дополнительная информация
            'transfer', 'health_issues', 'allergies',
            
            # Служебные поля
            'created_at', 'wave_id'
        ]
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

    def validate_birth_date(self, value):
        if value:
            from datetime import date
            if value > date.today():
                raise serializers.ValidationError("Дата рождения не может быть в будущем")
        # Можно добавить проверку возраста
            age = (date.today() - value).days // 365
            if age < 14:
                raise serializers.ValidationError("Посетитель должен быть старше 14 лет")
        return value

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
