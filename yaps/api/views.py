from rest_framework import generics, permissions
from yaps.models import *
from yaps.api.serializers import *
class YapListAPIView(generics.ListAPIView):
    queryset = Yap.objects.all().order_by('-criado_em')
    serializer_class = YapSerializer


class LikeCreateAPIView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class YapLikesListAPIView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        yap_id = self.kwargs['yap_id']
        return Like.objects.filter(yap__id=yap_id)



class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class YapCommentsListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        yap_id = self.kwargs['yap_id']
        return Comment.objects.filter(yap__id=yap_id).order_by('-criado_em')