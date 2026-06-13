from django.db import models
from django.conf import settings
from django.utils import timezone


class Desafio(models.Model):
    """
    Modelo de desafio do CommitClub.
    Representa um desafio que os usuários podem participar.
    """

    # Tipos de desafio
    TIPO_CHOICES = [
        ('DIARIO', 'Diário'),
        ('SEMANAL', 'Semanal'),
        ('MENSAL', 'Mensal'),
        ('CUSTOM', 'Personalizado'),
    ]

    # Categorias de desafio
    CATEGORIA_CHOICES = [
        ('PROGRAMACAO', 'Programação'),
        ('DESIGN', 'Design'),
        ('DADOS', 'Dados'),
        ('DEVOPS', 'DevOps'),
        ('ESTUDO', 'Estudo'),
        ('OUTRO', 'Outro'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    tipo = models.CharField(
        max_length=10, choices=TIPO_CHOICES, verbose_name='Tipo'
    )
    categoria = models.CharField(
        max_length=15, choices=CATEGORIA_CHOICES, verbose_name='Categoria'
    )
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='desafios_criados',
        verbose_name='Criador',
    )
    data_inicio = models.DateTimeField(verbose_name='Data de Início')
    data_fim = models.DateTimeField(verbose_name='Data de Fim')
    max_participantes = models.IntegerField(
        default=50, verbose_name='Máximo de Participantes'
    )
    xp_recompensa = models.IntegerField(
        default=50, verbose_name='XP de Recompensa'
    )
    coins_recompensa = models.DecimalField(
        max_digits=10, decimal_places=2, default=10,
        verbose_name='Moedas de Recompensa',
    )
    imagem = models.ImageField(
        upload_to='desafios/', null=True, blank=True, verbose_name='Imagem'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    publico = models.BooleanField(default=True, verbose_name='Público')
    roadmap_ia = models.JSONField(
        null=True, blank=True, verbose_name='Roadmap IA (Gemini)'
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Desafio'
        verbose_name_plural = 'Desafios'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

    @property
    def total_participantes(self):
        """Retorna o total de participantes no desafio."""
        return self.participacoes.count()

    @property
    def esta_ativo(self):
        """Verifica se o desafio está ativo e dentro do período válido."""
        agora = timezone.now()
        return self.ativo and self.data_inicio <= agora <= self.data_fim


class Participacao(models.Model):
    """
    Modelo de participação em um desafio.
    Relaciona um usuário a um desafio com progresso e status.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='participacoes',
        verbose_name='Usuário',
    )
    desafio = models.ForeignKey(
        Desafio,
        on_delete=models.CASCADE,
        related_name='participacoes',
        verbose_name='Desafio',
    )
    data_entrada = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Entrada'
    )
    progresso = models.IntegerField(
        default=0, verbose_name='Progresso (%)',
        help_text='Percentual de conclusão (0-100)',
    )
    concluido = models.BooleanField(default=False, verbose_name='Concluído')

    class Meta:
        verbose_name = 'Participação'
        verbose_name_plural = 'Participações'
        unique_together = ('usuario', 'desafio')

    def __str__(self):
        return f'{self.usuario.username} - {self.desafio.titulo}'


class Comprovacao(models.Model):
    """
    Modelo de comprovação de progresso em um desafio.
    Permite enviar evidências (arquivos, links) para validação.
    """

    participacao = models.ForeignKey(
        Participacao,
        on_delete=models.CASCADE,
        related_name='comprovacoes',
        verbose_name='Participação',
    )
    descricao = models.TextField(verbose_name='Descrição')
    arquivo = models.FileField(
        upload_to='comprovacoes/', null=True, blank=True,
        verbose_name='Arquivo',
    )
    link = models.URLField(blank=True, verbose_name='Link')
    aprovada = models.BooleanField(
        null=True, blank=True, verbose_name='Aprovada',
        help_text='None=Pendente, True=Aprovada, False=Rejeitada',
    )
    data_envio = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Envio'
    )

    class Meta:
        verbose_name = 'Comprovação'
        verbose_name_plural = 'Comprovações'
        ordering = ['-data_envio']

    def __str__(self):
        status = 'Pendente'
        if self.aprovada is True:
            status = 'Aprovada'
        elif self.aprovada is False:
            status = 'Rejeitada'
        return f'Comprovação ({status}) - {self.participacao}'
