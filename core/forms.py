
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'bio', 'profile_picture', 'display_name')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Adicione 'banner_picture' aos campos editáveis
        fields = ['display_name', 'bio', 'profile_picture', 'banner_picture']

class CustomAuthenticationForm(AuthenticationForm):
    pass