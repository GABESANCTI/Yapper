
from django.urls import path
from yaps.api import views
from yaps.api.views import YapListAPIView 
#por alguma razão o import do YapListAPIView não funciona com o from yaps.api.views import *
#não alterar isso até achar oq ue está acontecendo

urlpatterns = [
    #Lista todos os Yaps
    path('yaps/', YapListAPIView.as_view(), name='api_yap_list'),

    #Curtidas
    path('yaps/<int:yap_id>/likes/', views.YapLikesListAPIView.as_view(), name='yap_likes'),
    path('likes/create/', views.LikeCreateAPIView.as_view(), name='create_like'),

    #Comentários
    path('yaps/<int:yap_id>/comments/', views.YapCommentsListAPIView.as_view(), name='yap_comments'),
    path('comments/create/', views.CommentCreateAPIView.as_view(), name='create_comment'),
    #deletar Yap
    path('yaps/<int:pk>/delete/', views.YapDeleteAPIView.as_view(), name='delete_yap'),
]
