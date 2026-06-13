from django.db import models
from django.conf import settings


class Bolao(models.Model):
    """
    Modelo de bolão do CommitClub.
    Permite que usuários apostem moedas em desafios para ganhar prêmios.
    """

    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    desafio = models.ForeignKey(
        'desafios.Desafio',
        on_delete=models.SET_NULL,
        related_name='boloes',
        null=True,
        blank=True,
        verbose_name='Desafio Vinculado',
    )
    valor_entrada = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor de Entrada'
    )
    premio_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Prêmio Total',
    )
    criador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boloes_criados',
        verbose_name='Criador',
    )
    data_inicio = models.DateTimeField(verbose_name='Data de Início')
    data_fim = models.DateTimeField(verbose_name='Data de Fim')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    finalizado = models.BooleanField(default=False, verbose_name='Finalizado')
    publico = models.BooleanField(default=True, verbose_name='Público')
    
    REGRA_CHOICES = [
        ('TOP3', 'Top 3 (50% - 30% - 20%)'),
        ('WINNER', 'Só o 1º lugar (100%)')
    ]
    regra_distribuicao = models.CharField(
        max_length=10, choices=REGRA_CHOICES, default='TOP3',
        verbose_name='Distribuição do Prêmio'
    )
    
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Bolão'
        verbose_name_plural = 'Bolões'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

    @property
    def total_participantes(self):
        """Retorna o total de participantes no bolão."""
        return self.entradas.count()

    @property
    def status(self):
        if self.finalizado:
            return 'finalizado'
        if not self.ativo:
            return 'em_andamento'
        return 'aberto'

    @property
    def status_display(self):
        status_map = {
            'finalizado': 'Finalizado',
            'aberto': 'Aberto',
            'em_andamento': 'Em Andamento'
        }
        return status_map.get(self.status, self.status)


class EntradaBolao(models.Model):
    """
    Modelo de entrada (inscrição) em um bolão.
    Registra o pagamento do valor de entrada pelo usuário.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entradas_bolao',
        verbose_name='Usuário',
    )
    bolao = models.ForeignKey(
        Bolao,
        on_delete=models.CASCADE,
        related_name='entradas',
        verbose_name='Bolão',
    )
    valor_pago = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor Pago'
    )
    data_entrada = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Entrada'
    )

    class Meta:
        verbose_name = 'Entrada no Bolão'
        verbose_name_plural = 'Entradas nos Bolões'
        unique_together = ('usuario', 'bolao')

    def __str__(self):
        return f'{self.usuario.username} - {self.bolao.titulo}'


class Premiacao(models.Model):
    """
    Modelo de premiação de um bolão.
    Registra os prêmios distribuídos aos vencedores.
    """

    bolao = models.ForeignKey(
        Bolao,
        on_delete=models.CASCADE,
        related_name='premiacoes',
        verbose_name='Bolão',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='premiacoes',
        verbose_name='Usuário',
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Valor do Prêmio'
    )
    posicao = models.IntegerField(verbose_name='Posição')
    data_premiacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data da Premiação'
    )

    class Meta:
        verbose_name = 'Premiação'
        verbose_name_plural = 'Premiações'
        ordering = ['posicao']

    def __str__(self):
        return f'{self.posicao}º lugar - {self.usuario.username} ({self.bolao.titulo})'
