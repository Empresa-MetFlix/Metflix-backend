from rest_framework import serializers
from core.models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer para favoritos"""
    
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'media_id', 'created_at']
        read_only_fields = ['user', 'created_at']
