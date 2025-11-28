from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from core.serializers.token import CustomTokenObtainPairSerializer

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View customizada para obter token usando email
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Endpoint de registro de usuário
    """
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name', '')

    # Validações
    if not email or not password:
        return Response(
            {'detail': 'Email e senha são obrigatórios.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'detail': 'Este email já está em uso.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(password) < 6:
        return Response(
            {'detail': 'A senha deve ter pelo menos 6 caracteres.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # ✅ SIMPLIFICADO - Só passar email, password e name
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name  # ✅ Seu User model tem campo 'name'
        )

        return Response({
            'message': 'Usuário criado com sucesso!',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name or user.email
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'detail': f'Erro ao criar usuário: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
