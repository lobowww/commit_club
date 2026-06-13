from django.contrib import admin
from .models import Desafio, Participacao, Comprovacao


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    """Admin para o modelo de Desafio."""

    list_display = ['titulo', 'tipo', 'categoria', 'criador', 'data_inicio', 'data_fim', 'ativo']
    list_filter = ['tipo', 'categoria', 'ativo']
    search_fields = ['titulo', 'descricao']
    date_hierarchy = 'data_criacao'


@admin.register(Participacao)
class ParticipacaoAdmin(admin.ModelAdmin):
    """Admin para o modelo de Participação."""

    list_display = ['usuario', 'desafio', 'progresso', 'concluido', 'data_entrada']
    list_filter = ['concluido']
    search_fields = ['usuario__username', 'desafio__titulo']


@admin.register(Comprovacao)
class ComprovacaoAdmin(admin.ModelAdmin):
    """Admin para o modelo de Comprovação."""

    list_display = ['participacao', 'aprovada', 'data_envio']
    list_filter = ['aprovada']
    search_fields = ['descricao', 'participacao__usuario__username']
