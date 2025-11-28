from rest_framework import serializers
from core.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'avatar', 'is_kids', 'autoplay', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_name(self, value):
        """Validar nome do perfil"""
        if not value or not value.strip():
            raise serializers.ValidationError("O nome do perfil não pode estar vazio")
        
        if len(value) > 50:
            raise serializers.ValidationError("O nome do perfil é muito longo (máximo 50 caracteres)")
        
        return value.strip()
