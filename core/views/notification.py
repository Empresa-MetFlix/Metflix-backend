from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from core.models.notification import Notification
from core.serializers.notification import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar notificações do usuário
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas notificações do usuário logado"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Retorna contagem de notificações não lidas"""
        count = self.get_queryset().filter(read=False).count()
        return Response({'count': count})
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marca uma notificação como lida"""
        notification = self.get_object()
        notification.mark_as_read()
        
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Marca todas as notificações como lidas"""
        updated = self.get_queryset().filter(read=False).update(
            read=True,
            read_at=timezone.now()
        )
        return Response({
            'message': f'{updated} notificações marcadas como lidas',
            'updated_count': updated
        })
    
    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        """Limpa todas as notificações"""
        deleted = self.get_queryset().delete()
        return Response({
            'message': 'Todas as notificações foram removidas',
            'deleted_count': deleted[0]
        })
