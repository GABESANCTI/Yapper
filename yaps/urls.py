from django.urls import path
from .views import *
from .api.views import YapListAPIView

urlpatterns = [
    path('', timeline, name='timeline'),
    # rotas da nova api
    path('yaps/api/yaps/', YapListAPIView.as_view(), name='api_yaps'), 
]
