from rest_framework import generics, permissions
from yaps.models import *
from yaps.api.serializers import *
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
class YapListAPIView(generics.ListAPIView):
    queryset = Yap.objects.all().order_by('-criado_em')
    serializer_class = YapSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['autor__username']  # ou 'autor_id'


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
    

class YapDeleteAPIView(generics.DestroyAPIView):
    queryset = Yap.objects.all()
    serializer_class = YapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.autor != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este Yap.")
        instance.delete()

#204 No Content se for o autor.

#403 Forbidden se não for o autor.

 # autor só deleta seus próprios Yaps e comentarios
class YapDeleteAPIView(generics.DestroyAPIView):

    queryset = Yap.objects.all()
    serializer_class = YapSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
       
        return self.queryset.filter(autor=self.request.user)


class CommentDeleteAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Você não tem permissão para deletar este comentário.")
        instance.delete()