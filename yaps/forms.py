from django import forms
from .models import Yap, Comment

class YapForm(forms.ModelForm):
    class Meta:
        model = Yap
        
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que está acontecendo?'}),
        }
        labels = {
            'content': '',  # pra ignorar o lavel de 'content' como vazio
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Adicione um comentário...'}),
        }
        labels = {
            'content': '', 
        }