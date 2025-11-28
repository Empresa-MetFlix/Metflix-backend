from django.db import models
from .user import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=500)
    is_kids = models.BooleanField(default=False)
    autoplay = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'profiles'
        
    def __str__(self):
        return f"{self.user.email} - {self.name}"