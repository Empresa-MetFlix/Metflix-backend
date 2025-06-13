from django.db import models
from .cliente import Cliente
from .midia import Midia

class Reserva(models.Model):
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    midia = models.ForeignKey(Midia, on_delete=models.CASCADE)
    data_reserva = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.cliente.nome} - {self.midia.titulo}"