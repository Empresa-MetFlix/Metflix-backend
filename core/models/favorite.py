from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Favorite(models.Model):
    """
    Representa um filme ou série salvo na lista de favoritos de um usuário.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name="Usuário")
    # media_id é o ID único do filme/série na API externa (TMDb, etc.)
    media_id = models.CharField(max_length=50, verbose_name="ID da Mídia")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Garante que um usuário só possa adicionar o mesmo item uma vez
        unique_together = ('user', 'media_id',)
        ordering = ['-created_at']
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

    def __str__(self):
        # Apenas para fins de visualização no Admin, usa o email do usuário
        return f"{self.user.email} favoritou {self.media_id}"