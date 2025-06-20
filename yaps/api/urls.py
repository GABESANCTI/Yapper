
from django.urls import path
from .views import YapListAPIView

urlpatterns = [
    path('yaps/', YapListAPIView.as_view(), name='api_yap_list'),
]
