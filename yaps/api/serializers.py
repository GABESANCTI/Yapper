from rest_framework import serializers
from yaps.models import Yap, Like, Comment
from django.contrib.auth.models import User


class YapSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Yap
        fields = ['id', 'autor', 'conteudo', 'criado_em', 'likes_count', 'comments_count']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'yap', 'criado_em']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'yap', 'conteudo', 'criado_em']
