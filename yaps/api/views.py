from rest_framework import generics
from yaps.models import Yap
from yaps.api.serializers import YapSerializer

class YapListAPIView(generics.ListAPIView):
    queryset = Yap.objects.all().order_by('-criado_em')
    serializer_class = YapSerializer
