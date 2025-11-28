"""
User views.
"""
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User, Notification
from core.serializers.user import UserSerializer
from core.services.email_service import EmailService

import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter to only return current user."""
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Get current user."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request):
        """
        Deleta a conta do usuário autenticado.
        Requer confirmação via password.
        """
        try:
            password = request.data.get('password')
            
            if not password:
                return Response(
                    {'error': 'Senha é obrigatória para confirmar exclusão'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = request.user
            
            if not user.check_password(password):
                return Response(
                    {'error': 'Senha incorreta'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            user_email = user.email
            user_name = EmailService._get_user_name(user)
            
            user.delete()
            
            logger.info(f"🗑️ Conta deletada: {user_email}")
            
            try:
                email_service = EmailService()
                email_service.send_account_deleted_email(user_email, user_name)
            except Exception as email_error:
                logger.error(f"❌ Erro ao enviar email de exclusão: {str(email_error)}")
            
            return Response(
                {'message': 'Conta deletada com sucesso'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao deletar conta: {str(e)}")
            return Response(
                {'error': 'Erro ao deletar conta. Tente novamente.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Registrar novo usuário.
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')

        # Validações
        if not email:
            return Response(
                {'error': 'Email é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {'error': 'Senha é obrigatória'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(password) < 4:
            return Response(
                {'error': 'Senha deve ter no mínimo 4 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Este email já está cadastrado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar usuário
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name if name else None
        )

        logger.info(f"✅ Novo usuário criado: {user.email}")

        # ✅ CRIAR NOTIFICAÇÃO DE BOAS-VINDAS
        try:
            Notification.objects.create(
                user=user,
                title='Bem-vindo ao Metflix!',
                message='Sua conta foi criada com sucesso! Comece a explorar nosso catálogo.',
                notification_type='system',
                link='/'
            )
            logger.info(f"📱 Notificação de boas-vindas criada para: {user.email}")
        except Exception as notif_error:
            logger.error(f"❌ Erro ao criar notificação: {str(notif_error)}")

        # ✅ ENVIAR EMAIL DE BOAS-VINDAS (SÍNCRONO MAS SEM BLOQUEAR)
        try:
            logger.info(f"📧 Tentando enviar email de boas-vindas para: {user.email}")
            email_service = EmailService()
            email_sent = email_service.send_welcome_email(user)
            
            if email_sent:
                logger.info(f"✅ Email de boas-vindas ENVIADO para: {user.email}")
            else:
                logger.warning(f"⚠️ Email de boas-vindas NÃO enviado para: {user.email}")
                
        except Exception as email_error:
            logger.error(f"❌ ERRO ao enviar email de boas-vindas: {str(email_error)}")
            import traceback
            logger.error(traceback.format_exc())

        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Usuário criado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"❌ Erro ao registrar usuário: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return Response(
            {'error': 'Erro ao criar usuário. Tente novamente.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
