from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import User


class UserSerializer(ModelSerializer):
    """Serializer for the user object."""

    # 1. Adiciona o campo 'password'
    password = serializers.CharField(
        style={'input_type': 'password'}, # Ajuda na documentação
        trim_whitespace=False,             # Permite espaços em branco
        write_only=True                    # MUITO IMPORTANTE: Garante que a senha não seja retornada na resposta GET
    )

    class Meta:
        model = User
        # 2. Adiciona 'password' aos campos
        fields = ["id", "email", "name", "password", "is_active", "is_staff"]
        # Campos que devem ser apenas de leitura (não podem ser alterados pelo usuário)
        read_only_fields = ["is_active", "is_staff"]


    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        
        # 3. CRÍTICO: Usa o método create_user do UserManager para garantir o hash da senha
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name')
        )
        
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        
        # 4. TRATAMENTO DA SENHA NA ATUALIZAÇÃO:
        # Pega a senha dos dados validados (se existir)
        password = validated_data.pop('password', None)
        
        # Chama a implementação padrão para atualizar todos os outros campos
        user = super().update(instance, validated_data)

        # Se a senha foi fornecida, atualiza-a de forma segura
        if password:
            user.set_password(password)
            user.save()

        return user
