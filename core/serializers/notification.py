from rest_framework import serializers
from core.models.notification import Notification
from django.utils.timesince import timesince

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer para notificações"""
    
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'link',
            'metadata',
            'read',
            'created_at',
            'read_at',
            'time_ago',
        ]
        read_only_fields = ['created_at', 'read_at']
    
    def get_time_ago(self, obj):
        """Retorna tempo relativo (ex: 'há 2 horas')"""
        return f"há {timesince(obj.created_at)}"
