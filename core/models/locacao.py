from django.db import models
from .cliente import Cliente  

class Locacao(models.Model):
    STATUS_CHOICES = (
        ('aberta', 'Aberta'),
        ('fechada', 'Fechada'),
        ('atrasada', 'Atrasada'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_retirada = models.DateField()
    data_prevista_devolucao = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Locacao {self.id} - {self.cliente.nome}"