from django.db import models
from django.conf import settings # Para referenciar o modelo de usuário do projet

class Yap(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='yaps')
    content = models.TextField(max_length=280) # Limite de caracteres como no Twitter
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)

    # A funcionalidade de likes será gerenciada inteiramente pelo modelo 'Like' explícito.
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_yaps', blank=True)

    class Meta:
        ordering = ['-created_at'] # Ordena os yaps pelo mais recente

    def __str__(self):
        return f"Yap by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class Comment(models.Model):
    yap = models.ForeignKey(Yap, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Ordena os comentários pelo mais antigo

    def __str__(self):
        return f"Comment by {self.user.username} on Yap {self.yap.id}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    yap = models.ForeignKey(Yap, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('user', 'yap'), ('user', 'comment')
        ordering = ['-created_at'] 

    def __str__(self):
        if self.yap:
            return f"User {self.user.username} liked Yap {self.yap.id}"
        elif self.comment:
            return f"User {self.user.username} liked Comment {self.comment.id}"
        return f"User {self.user.username} liked something unknown" # Caso para depuração