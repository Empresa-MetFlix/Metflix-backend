from django.db import models

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    cargo = models.CharField(max_length=50)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
