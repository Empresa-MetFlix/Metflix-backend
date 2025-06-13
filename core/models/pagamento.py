from django.db import models
from .locacao import Locacao

class Pagamento(models.Model):
    METODO_CHOICES = (
        ('credito', 'Cartão de Crédito'),
        ('debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
    )

    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE)
    valor_aluguel = models.DecimalField(max_digits=8, decimal_places=2)
    valor_multa = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateField(auto_now_add=True)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)

    def __str__(self):
        return f"Pagamento {self.id} - Locacao {self.locacao.id}"
