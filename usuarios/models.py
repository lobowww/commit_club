from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuário customizado do CommitClub.
    Estende o AbstractUser com campos de gamificação, perfil e carteira virtual.
    """

    # Perfil
    bio = models.TextField(blank=True, verbose_name='Biografia')
    avatar = models.ImageField(
        upload_to='avatars/', null=True, blank=True, verbose_name='Avatar'
    )
    github_username = models.CharField(
        max_length=100, blank=True, verbose_name='Usuário GitHub'
    )
    linkedin_url = models.URLField(blank=True, verbose_name='LinkedIn')

    # Gamificação
    nivel = models.IntegerField(default=1, verbose_name='Nível')
    xp = models.IntegerField(default=0, verbose_name='Experiência (XP)')
    saldo_reais = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name='Saldo (R$)'
    )

    # Streaks
    streak_atual = models.IntegerField(
        default=0, verbose_name='Streak Atual (dias)'
    )
    maior_streak = models.IntegerField(
        default=0, verbose_name='Maior Streak (dias)'
    )

    # Tipo de conta
    is_empresa = models.BooleanField(
        default=False, verbose_name='É Empresa?'
    )

    # Timestamps
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação'
    )

    # Onboarding
    onboarding_completo = models.BooleanField(
        default=False, verbose_name='Onboarding Completo'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    @property
    def progresso_nivel(self):
        """Retorna o progresso percentual para o próximo nível (0-99)."""
        return self.xp % 100

    def adicionar_xp(self, quantidade):
        """
        Adiciona XP ao usuário.
        - Incrementa o nível quando xp >= nivel * 100
        - Adiciona 1 moeda a cada 10 XP ganhos
        """
        self.xp += quantidade

        # Subir de nível enquanto XP for suficiente
        while self.xp >= self.nivel * 100:
            self.xp -= self.nivel * 100
            self.nivel += 1

        self.save()
