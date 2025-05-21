from django import forms
from .models import Yap
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User #modelo padrao do django de usuario, alterar depois (incluir-> display_name)
        fields = ['username', 'email', 'password1', 'password2']

class YapForm(forms.ModelForm):
    class Meta:
        model = Yap
        fields = ['conteudo']
        widgets = {
        'conteudo': forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'Compartilhe algo com a galera...',
        'class': 'form-control'}),}

