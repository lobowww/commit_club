from django.db import models
from django.conf import settings


class Empresa(models.Model):
    """
    Modelo de empresa parceira do CommitClub.
    Vinculada a um usuário com is_empresa=True.
    """

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='empresa',
        verbose_name='Usuário',
    )
    nome_empresa = models.CharField(
        max_length=200, verbose_name='Nome da Empresa'
    )
    cnpj = models.CharField(
        max_length=18, blank=True, verbose_name='CNPJ'
    )
    descricao = models.TextField(
        blank=True, verbose_name='Descrição'
    )
    logo = models.ImageField(
        upload_to='empresas/', null=True, blank=True, verbose_name='Logo'
    )
    site = models.URLField(blank=True, verbose_name='Site')
    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.nome_empresa


class DesafioEmpresa(models.Model):
    """
    Modelo de desafio patrocinado por uma empresa.
    Permite que empresas patrocinem desafios e ofereçam vagas de emprego.
    """

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='desafios_empresa',
        verbose_name='Empresa',
    )
    desafio = models.ForeignKey(
        'desafios.Desafio',
        on_delete=models.CASCADE,
        related_name='empresa_patrocinadora',
        verbose_name='Desafio',
    )
    patrocinio = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Valor do Patrocínio',
    )
    vagas_emprego = models.BooleanField(
        default=False, verbose_name='Oferece Vagas de Emprego'
    )
    link_vaga = models.URLField(
        blank=True, verbose_name='Link da Vaga'
    )
    
    # B2B Configs
    stack_avaliada = models.CharField(
        max_length=200, blank=True, verbose_name='Tecnologia / Stack avaliada'
    )
    duracao_dias = models.IntegerField(
        default=14, verbose_name='Duração do desafio (dias)'
    )
    max_candidatos = models.IntegerField(
        default=20, verbose_name='Máx. de candidatos'
    )
    NIVEL_CHOICES = [
        ('Junior', 'Júnior'),
        ('Pleno', 'Pleno'),
        ('Senior', 'Sênior'),
    ]
    nivel_exigido = models.CharField(
        max_length=20, choices=NIVEL_CHOICES, default='Pleno',
        verbose_name='Nível exigido'
    )
    
    # Métricas
    metrica_consistencia = models.BooleanField(
        default=True, verbose_name='Consistência diária (ofensiva)'
    )
    metrica_qualidade_ia = models.BooleanField(
        default=True, verbose_name='Qualidade de commits (IA)'
    )
    metrica_tempo = models.BooleanField(
        default=True, verbose_name='Tempo médio de entrega'
    )
    metrica_score = models.BooleanField(
        default=False, verbose_name='Score de disciplina'
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True, verbose_name='Data de Criação'
    )

    class Meta:
        verbose_name = 'Desafio de Empresa'
        verbose_name_plural = 'Desafios de Empresas'

    def __str__(self):
        return f'{self.empresa.nome_empresa} - {self.desafio.titulo}'
