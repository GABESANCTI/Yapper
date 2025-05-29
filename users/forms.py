from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#revisar o nome do campo senha e confirmar_senha, pois o Django já possui um campo senha padrão
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
