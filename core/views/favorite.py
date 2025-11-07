from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# Importa o modelo e o serializer usando o caminho relativo (.. significa core)
from ..models import Favorite
from ..serializers import FavoriteSerializer 

User = get_user_model()

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar os favoritos do usuário (Minha Lista).
    Permite Listar (GET), Criar (POST) e Deletar (DELETE) favoritos.
    A rota será exposta como /api/me/favorites/.
    """
    # 1. ATRIBUIÇÃO DO SERIALIZER
    serializer_class = FavoriteSerializer
    
    # Garante que apenas usuários autenticados possam acessar esta View
    permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        """
        Retorna apenas os objetos Favorite que pertencem ao usuário logado.
        Isto garante a segurança e isolamento da lista.
        """
        # Filtra a lista pelo usuário atual
        if self.request.user.is_authenticated:
            return Favorite.objects.filter(user=self.request.user)
        return Favorite.objects.none()

    def perform_create(self, serializer):
        """
        Define o usuário logado como o proprietário do novo registro Favorite
        antes de salvar no banco de dados, e trata duplicatas.
        """
        try:
            # Salva o favorito e associa ao usuário logado
            serializer.save(user=self.request.user)
        except Exception as e:
            # Trata o erro de restrição de unicidade (se o item já foi favoritado)
            if 'unique constraint' in str(e).lower() or 'duplicate key' in str(e).lower():
                return Response(
                    {"detail": "Este item já está na sua lista."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Re-lança outras exceções
            raise