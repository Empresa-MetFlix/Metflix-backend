from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers.token import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """View customizada para login com email"""
    serializer_class = CustomTokenObtainPairSerializer
