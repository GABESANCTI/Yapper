from django.db import models
from django.contrib.auth.models import User

class Yap(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor.username}: {self.conteudo[:30]}'
