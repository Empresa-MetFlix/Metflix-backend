from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer para usar email no login em vez de username"""
    username_field = 'email'
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adiciona claims customizados ao token
        token['email'] = user.email
        token['name'] = user.name
        return token
