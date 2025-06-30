
from django.urls import path
from . import views

app_name = 'core' # Namespace para as URLs do app core

urlpatterns = [
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('<str:username>/follow/', views.follow_user, name='follow_user'),
    path('<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
]