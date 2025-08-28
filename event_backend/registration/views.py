from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Visitor, EventWave
from .serializers import VisitorSerializer, EventWaveSerializer
from .services.blacklist_service import BlackListService

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    

class EventWaveViewSet(viewsets.ModelViewSet):
    queryset = EventWave.objects.all()
    serializer_class = EventWaveSerializer
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        wave = self.get_object()
        wave.is_active = not wave.is_active
        wave.save()
        return Response({'is_active': wave.is_active})

class BlackListView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def sync_blacklist(self, request):
        blacklist_service = BlackListService()
        success, message = blacklist_service.sync_blacklist()
        
        if success:
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'error': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def check_visitor(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        middle_name = request.data.get('middle_name', '')
        
        if not first_name or not last_name:
            return Response(
                {'error': 'Необходимо указать имя и фамилию'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        blacklist_service = BlackListService()
        is_blacklisted, reason = blacklist_service.check_blacklist(first_name, last_name, middle_name)
        
        return Response({
            'is_blacklisted': is_blacklisted,
            'reason': reason
        })
