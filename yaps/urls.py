from django.urls import path
from . import views

app_name = 'yaps' # Namespace para as URLs do app yaps

urlpatterns = [
    path('', views.general_timeline, name='general_timeline'), # Timeline geral (home)
    path('foryou/', views.foryou_timeline, name='foryou_timeline'), # For You Page
    path('yap/create/', views.create_yap, name='create_yap'),
    path('yap/<int:pk>/', views.yap_detail, name='yap_detail'),
    path('yap/<int:pk>/delete/', views.delete_yap, name='delete_yap'),
    path('yap/<int:pk>/like/', views.like_yap, name='like_yap'),
    #path('yap/<int:pk>/unlike/', views.unlike_yap, name='unlike_yap'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    #path('comment/<int:pk>/unlike/', views.unlike_comment, name='unlike_comment'),
     # Curtir Comentários (com AJAX)
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    
    # Apagar Comentário
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment')
]