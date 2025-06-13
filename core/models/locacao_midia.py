from django.db import models
from .locacao import Locacao
from .midia import Midia  # Certifique que exista o modelo Midia

class LocacaoMidia(models.Model):
    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE)
    midia = models.ForeignKey(Midia, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Locacao {self.locacao.id} - Mídia: {self.midia.titulo} (Qtd: {self.quantidade})"