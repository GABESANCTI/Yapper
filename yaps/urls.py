from django.urls import path
from .views import *

urlpatterns = [
    path('', timeline, name='timeline'),
    path('/', timeline, name='timeline'),
]
