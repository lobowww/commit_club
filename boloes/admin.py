from django.contrib import admin
from .models import Bolao, EntradaBolao, Premiacao


@admin.register(Bolao)
class BolaoAdmin(admin.ModelAdmin):
    """Admin para o modelo de Bolão."""

    list_display = ['titulo', 'criador', 'valor_entrada', 'premio_total', 'ativo', 'finalizado']
    list_filter = ['ativo', 'finalizado']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_criacao'


@admin.register(EntradaBolao)
class EntradaBolaoAdmin(admin.ModelAdmin):
    """Admin para o modelo de Entrada no Bolão."""

    list_display = ['usuario', 'bolao', 'valor_pago', 'data_entrada']
    search_fields = ['usuario__username', 'bolao__titulo']


@admin.register(Premiacao)
class PremiacaoAdmin(admin.ModelAdmin):
    """Admin para o modelo de Premiação."""

    list_display = ['bolao', 'usuario', 'valor', 'posicao', 'data_premiacao']
    list_filter = ['posicao']
    search_fields = ['usuario__username', 'bolao__titulo']
