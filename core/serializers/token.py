from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado para aceitar email ao invés de username
    """
    email = serializers.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({
                'detail': 'Email e senha são obrigatórios.'
            })

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({
                'detail': 'Email ou senha incorretos.'
            })

        if not user.is_active:
            raise serializers.ValidationError({
                'detail': 'Usuário inativo.'
            })

        refresh = self.get_token(user)

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name or user.email,  # ✅ Usar 'name' ao invés de 'get_full_name()'
                'is_staff': user.is_staff,
                'is_active': user.is_active
            }
        }

        return data
