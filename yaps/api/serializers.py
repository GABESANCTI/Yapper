from rest_framework import serializers
from models import Yap

class YapSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Yap
        fields = ['id', 'author', 'conteudo', 'criado_em']
