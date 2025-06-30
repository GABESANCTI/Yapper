
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'bio', 'profile_picture') # Inclua os campos adicionais do seu modelo User

class CustomAuthenticationForm(AuthenticationForm):

    pass