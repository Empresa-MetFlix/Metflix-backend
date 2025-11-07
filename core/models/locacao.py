from django.conf import settings
from django.db import models
from django.utils import timezone

# IMPORTANTE: A classe LocacaoMidia FOI REMOVIDA DESTE ARQUIVO.
# Certifique-se de que ela está definida APENAS em core/models/locacao_midia.py.

class Locacao(models.Model):
    """
    Modelo principal para registrar uma Locação (aluguel) de mídias.
    Este modelo contém as informações gerais da transação.
    """
    
    # Assumindo que o cliente está relacionado ao modelo de usuário padrão (settings.AUTH_USER_MODEL)
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        related_name='locacoes',
        verbose_name='Cliente'
    )
    
    data_locacao = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Data de Locação'
    )
    
    # A data em que o item deve ser devolvido
    data_devolucao_prevista = models.DateField(
        verbose_name='Data de Devolução Prevista'
    )
    
    # A data em que o item foi de fato devolvido (null se a locação estiver ativa)
    data_devolucao_real = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name='Data de Devolução Realizada'
    )
    
    @property
    def esta_ativa(self):
        """Verifica se a locação ainda não foi concluída."""
        return self.data_devolucao_real is None

    class Meta:
        verbose_name = "Locação"
        verbose_name_plural = "Locações"
        ordering = ['-data_locacao']

    def __str__(self):
        return f"Locação #{self.id} (Cliente: {self.cliente.username})"