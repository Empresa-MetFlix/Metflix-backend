from django.db import models
from .genero import Genero

class Midia(models.Model):
    titulo = models.CharField(max_length=200)
    genero = models.ForeignKey(Genero, on_delete=models.PROTECT)
    ano = models.PositiveIntegerField()
    classificacao_indicativa = models.CharField(max_length=20)
    quantidade = models.PositiveIntegerField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
