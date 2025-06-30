# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('register/', views.register, name='register'),

    # URL para a página de perfil
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    # URLs para seguir/deixar de seguir (agora dentro do caminho 'profile/')
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
]