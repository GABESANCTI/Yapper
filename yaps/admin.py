from django.contrib import admin
from .models import Yap

@admin.register(Yap)
class YapAdmin(admin.ModelAdmin):
    list_display = ('autor', 'conteudo', 'criado_em')
    search_fields = ('autor__username', 'conteudo')
    list_filter = ('criado_em',)
