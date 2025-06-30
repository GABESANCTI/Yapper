
from django import forms
from .models import Yap, Comment

class YapForm(forms.ModelForm):
    class Meta:
        model = Yap
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O que está acontecendo?'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Adicione um comentário...'}),
        }