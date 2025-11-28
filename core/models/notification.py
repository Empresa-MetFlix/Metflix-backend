from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    """
    Modelo para notificações do usuário
    """
    NOTIFICATION_TYPES = [
        ('new_content', 'Novo Conteúdo'),
        ('favorite_added', 'Adicionado aos Favoritos'),
        ('recommendation', 'Recomendação'),
        ('system', 'Sistema'),
        ('achievement', 'Conquista'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name="Usuário"
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='system',
        verbose_name="Tipo"
    )
    
    title = models.CharField(max_length=200, verbose_name="Título")
    message = models.TextField(verbose_name="Mensagem")
    
    # Link relacionado (opcional)
    link = models.CharField(max_length=500, blank=True, null=True, verbose_name="Link")
    
    # Dados extras em JSON (ex: movie_id, poster_url, etc)
    metadata = models.JSONField(blank=True, null=True, verbose_name="Metadados")
    
    # Status
    read = models.BooleanField(default=False, verbose_name="Lida")
    sent_email = models.BooleanField(default=False, verbose_name="Email Enviado")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    read_at = models.DateTimeField(blank=True, null=True, verbose_name="Lida em")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'read']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
    
    def mark_as_read(self):
        """Marca notificação como lida"""
        from django.utils import timezone
        if not self.read:
            self.read = True
            self.read_at = timezone.now()
            self.save(update_fields=['read', 'read_at'])
