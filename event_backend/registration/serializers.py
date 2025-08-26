from rest_framework import serializers
from .models import Visitor, EventWave
from .services.blacklist_service import BlackListService

class VisitorSerializer(serializers.ModelSerializer):
    wave_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Visitor
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'vk_link', 'created_at', 'wave_id']
    
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

class EventWaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventWave
        fields = '__all__'
