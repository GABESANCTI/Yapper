from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
