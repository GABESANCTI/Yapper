
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'bio', 'profile_picture', 'display_name') # Adicione 'display_name'

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Defina quais campos o usuário pode editar no perfil
        fields = ['display_name', 'bio', 'profile_picture']

class CustomAuthenticationForm(AuthenticationForm):
    pass