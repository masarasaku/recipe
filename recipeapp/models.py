from django.db import models
from django.contrib.auth.models import User

class UserSeasoning(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seasoning')
    saved_seasoning = models.TextField(blank=True, default="", help_text="保存された調味料リスト")
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}の調味料リスト"

# Create your models here.
