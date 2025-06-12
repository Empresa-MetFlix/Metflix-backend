from django.db import models
from django.conf import settings

class Rental(models.Model):
    """Locações feitas por usuários."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='rentals'
    )
    media = models.ForeignKey(
        'Media',
        on_delete=models.CASCADE,
        verbose_name='Mídia',
        related_name='rentals'
    )
    rented_at = models.DateTimeField(auto_now_add=True, verbose_name='Data da locação')
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name='Data de devolução')

    class Meta:
        verbose_name = 'Locação'
        verbose_name_plural = 'Locações'

    def __str__(self):
        return f'{self.media.title} - {self.user.email}'
