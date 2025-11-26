from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from ..models import Favorite
from ..serializers import FavoriteSerializer

User = get_user_model()


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar favoritos do usuário (Minha Lista).
    Rotas: /api/favorites/
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas favoritos do usuário logado"""
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user).select_related('midia')
        return Favorite.objects.none()
    
    def create(self, request, *args, **kwargs):
        """Cria um novo favorito com tratamento de duplicatas"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Salva com o usuário logado
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"detail": "Este item já está na sua lista."},
                status=status.HTTP_400_BAD_REQUEST
            )
