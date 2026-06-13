from django.contrib import admin
from .models import Empresa, DesafioEmpresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    """Admin para o modelo de Empresa."""

    list_display = ['nome_empresa', 'usuario', 'cnpj', 'site', 'data_criacao']
    search_fields = ['nome_empresa', 'cnpj', 'usuario__username']


@admin.register(DesafioEmpresa)
class DesafioEmpresaAdmin(admin.ModelAdmin):
    """Admin para o modelo de Desafio de Empresa."""

    list_display = ['empresa', 'desafio', 'patrocinio', 'vagas_emprego', 'data_criacao']
    list_filter = ['vagas_emprego']
    search_fields = ['empresa__nome_empresa', 'desafio__titulo']
