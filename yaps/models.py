from django.db import models
from django.contrib.auth.models import User

class Yap(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.autor.username}: {self.conteudo[:30]}'
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yap = models.ForeignKey(Yap, on_delete=models.CASCADE, related_name='likes')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'yap')
    def __str__(self):
        return f'{self.user.username} curtiu o Yap! {self.yap.id}'
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yap = models.ForeignKey(Yap, on_delete=models.CASCADE, related_name='comments')
    conteudo = models.TextField(max_length=280)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} comentou: {self.conteudo[:30]}'