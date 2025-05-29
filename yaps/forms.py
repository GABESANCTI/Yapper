from django import forms
from .models import Yap

class YapForm(forms.ModelForm):
    class Meta:
        model = Yap
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'No que está pensando?'}),
        }
