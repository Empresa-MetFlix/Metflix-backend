from django.db import models
class Media(models.Model):
    """Mídia disponível para locação."""
    title = models.CharField(max_length=255, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descrição')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Categoria',
        related_name='medias'
    )
    release_year = models.PositiveIntegerField(verbose_name='Ano de lançamento')
    is_available = models.BooleanField(default=True, verbose_name='Disponível')

    class Meta:
        verbose_name = 'Mídia'
        verbose_name_plural = 'Mídias'

    def __str__(self):
        return self.title
