from django import forms
from .models import Yap

class YapForm(forms.ModelForm):
    class Meta:
        model = Yap
        fields = ['conteudo']
        widgets = {
        'conteudo': forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Compartilhe algo com a galera...',
        'class': 'form-control'}),}

