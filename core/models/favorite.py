from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Favorite(models.Model):
    """
    Representa um filme ou série salvo na lista de favoritos de um usuário.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorites', 
        verbose_name="Usuário"
    )
    
    # ✅ ID externo da API TMDB
    media_id = models.CharField(
        max_length=50, 
        verbose_name="ID da Mídia"
    )
    
    # ✅ NOVO: Tipo de mídia (filme ou série)
    media_type = models.CharField(
        max_length=20,
        default='movie',
        choices=[
            ('movie', 'Filme'),
            ('tv', 'Série')
        ],
        verbose_name='Tipo de Mídia'
    )
    
    # ✅ NOVO: Título da mídia (para exibir sem chamar API)
    media_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Título'
    )
    
    # ✅ NOVO: Caminho do poster (para exibir sem chamar API)
    media_poster_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Caminho do Poster'
    )
    
    # ✅ Campo de data de criação
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    
    class Meta:
        # ✅ ATUALIZADO: Unique para user + media_id + media_type
        unique_together = ('user', 'media_id', 'media_type',)
        ordering = ['-created_at']
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
    
    def __str__(self):
        return f"{self.user.email} - {self.media_title or f'Mídia {self.media_id}'}"
