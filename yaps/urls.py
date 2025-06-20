from django.urls import path
from .views import *
from .api.views import YapListAPIView
from django.urls import include

urlpatterns = [
    path('', timeline, name='timeline'),
    # rotas da nova api
    path('yaps/api/yaps/', YapListAPIView.as_view(), name='api_yaps'),
    # rotas da api de usuários
]
