from django.urls import path
from users.api.views import UserYapsAPIView

urlpatterns = [
    path('users/<str:username>/yaps/', UserYapsAPIView.as_view(), name='user-yaps'),
]
