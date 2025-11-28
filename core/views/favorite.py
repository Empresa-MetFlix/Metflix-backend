"""
Favorite views.
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from core.models import Favorite, Notification
from core.serializers.favorite import FavoriteSerializer
from core.services.email_service import EmailService

import logging

logger = logging.getLogger(__name__)


class FavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user favorites."""
    
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the current user's favorites."""
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """
        Cria um novo favorito para o usuário.
        
        Também envia email e cria notificação.
        """
        try:
            media_id = request.data.get('media_id')
            media_type = request.data.get('media_type', 'movie')
            media_title = request.data.get('media_title', 'Conteúdo')
            
            # Verificar se já existe
            if Favorite.objects.filter(
                user=request.user,
                media_id=media_id,
                media_type=media_type
            ).exists():
                return Response(
                    {'error': 'Este item já está na sua lista'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Criar favorito
            favorite = Favorite.objects.create(
                user=request.user,
                media_id=media_id,
                media_type=media_type,
                media_title=media_title,
                media_poster_path=request.data.get('media_poster_path', '')
            )
            
            logger.info(f"✅ Favorito criado: {media_title} por {request.user.email}")
            
            # Definir tipo de mídia
            media_type_display = 'série' if media_type == 'tv' else 'filme'
            
            # ✅ CRIAR NOTIFICAÇÃO NO BANCO (APARECE NO NAVBAR)
            try:
                notification = Notification.objects.create(
                    user=request.user,
                    title='Adicionado à Minha Lista',
                    message=f'{media_title} foi adicionado à sua lista de favoritos!',
                    notification_type='favorite_added',
                    link='/minha-lista'
                )
                
                logger.info(f"📱 Notificação criada no banco para: {request.user.email}")
            except Exception as notif_error:
                logger.error(f"❌ Erro ao criar notificação: {str(notif_error)}")
            
            # ✅ ENVIAR EMAIL (NÃO BLOQUEIA)
            try:
                email_service = EmailService()
                email_service.send_favorite_added_email(
                    user=request.user,
                    media_title=media_title,
                    media_type=media_type_display,
                    media_id=media_id
                )
                
                logger.info(f"📧 Email de favorito enviado para: {request.user.email}")
            except Exception as email_error:
                logger.error(f"❌ Erro ao enviar email: {str(email_error)}")
            
            serializer = self.get_serializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar favorito: {str(e)}")
            return Response(
                {'error': 'Erro ao adicionar à lista'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def destroy(self, request, *args, **kwargs):
        """Remove um favorito da lista do usuário."""
        try:
            instance = self.get_object()
            media_title = instance.media_title
            
            self.perform_destroy(instance)
            
            logger.info(f"🗑️ Favorito removido: {media_title} por {request.user.email}")
            
            return Response(
                {'message': 'Removido da sua lista'},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao remover favorito: {str(e)}")
            return Response(
                {'error': 'Erro ao remover da lista'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def check(self, request):
        """
        Verifica se um filme/série está nos favoritos.
        
        Query params: media_id, media_type
        """
        media_id = request.query_params.get('media_id')
        media_type = request.query_params.get('media_type', 'movie')
        
        if not media_id:
            return Response(
                {'error': 'media_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_favorite = Favorite.objects.filter(
            user=request.user,
            media_id=media_id,
            media_type=media_type
        ).exists()
        
        return Response({'is_favorite': is_favorite})
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """
        Toggle favorito (adiciona ou remove).
        
        Também cria notificação se adicionar.
        """
        try:
            media_id = request.data.get('media_id')
            media_type = request.data.get('media_type', 'movie')
            media_title = request.data.get('title', 'Conteúdo')
            
            if not media_id:
                return Response(
                    {'error': 'media_id é obrigatório'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar se já existe
            favorite = Favorite.objects.filter(
                user=request.user,
                media_id=str(media_id),
                media_type=media_type
            ).first()
            
            if favorite:
                # ✅ REMOVER
                favorite.delete()
                logger.info(f"🗑️ Favorito removido: {media_title} por {request.user.email}")
                
                return Response({
                    'action': 'removed',
                    'message': 'Removido da sua lista'
                })
            else:
                # ✅ ADICIONAR
                favorite = Favorite.objects.create(
                    user=request.user,
                    media_id=str(media_id),
                    media_type=media_type,
                    media_title=media_title,
                    media_poster_path=request.data.get('media_poster_path', '')
                )
                
                logger.info(f"✅ Favorito criado: {media_title} por {request.user.email}")
                
                # ✅ CRIAR NOTIFICAÇÃO (APARECE NO NAVBAR)
                try:
                    media_type_display = 'série' if media_type == 'tv' else 'filme'
                    
                    Notification.objects.create(
                        user=request.user,
                        title='Adicionado à Minha Lista',
                        message=f'{media_title} foi adicionado à sua lista de favoritos!',
                        notification_type='favorite_added',
                        link='/minha-lista'
                    )
                    
                    logger.info(f"📱 Notificação criada para: {request.user.email}")
                except Exception as notif_error:
                    logger.error(f"❌ Erro ao criar notificação: {str(notif_error)}")
                
                # ✅ ENVIAR EMAIL (NÃO BLOQUEIA)
                try:
                    email_service = EmailService()
                    email_service.send_favorite_added_email(
                        user=request.user,
                        media_title=media_title,
                        media_type=media_type_display,
                        media_id=media_id
                    )
                    
                    logger.info(f"📧 Email de favorito enviado para: {request.user.email}")
                except Exception as email_error:
                    logger.error(f"❌ Erro ao enviar email: {str(email_error)}")
                
                serializer = self.get_serializer(favorite)
                
                return Response({
                    'action': 'added',
                    'message': 'Adicionado à sua lista',
                    'favorite': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            logger.error(f"❌ Erro ao toggle favorito: {str(e)}")
            return Response(
                {'error': 'Erro ao processar favorito'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
