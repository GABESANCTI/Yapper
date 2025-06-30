
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    display_name = models.CharField(max_length=50, blank=True, null=True)  # Nome de exibição opcional
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_views = models.PositiveIntegerField(default=0) # Contador de visualizações

    # Relação de seguidores/seguindo
    # symmetrical=False permite que A siga B sem que B siga A automaticamente
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username