from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin customizado para o modelo de Usuário."""

    list_display = ['username', 'email', 'nivel', 'xp', 'saldo_reais', 'is_empresa']
    list_filter = ['is_empresa', 'nivel', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'github_username']

    # Adiciona os campos customizados ao formulário do admin
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil', {
            'fields': ('bio', 'avatar', 'github_username', 'linkedin_url'),
        }),
        ('Gamificação', {
            'fields': ('nivel', 'xp', 'saldo_reais', 'streak_atual', 'maior_streak'),
        }),
        ('Tipo de Conta', {
            'fields': ('is_empresa',),
        }),
    )
