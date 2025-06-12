from django.db import models

class Category(models.Model):
    """Categoria de mídias (ex: Ação, Drama, Comédia)."""
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name