from rest_framework import generics
from yaps.models import Yap
from yaps.api.serializers import YapSerializer

class UserYapsAPIView(generics.ListAPIView):
    serializer_class = YapSerializer

    def get_queryset(self):
        username = self.kwargs['username']
        return Yap.objects.filter(autor__username=username).order_by('-criado_em')
