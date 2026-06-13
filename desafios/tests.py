from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Desafio

Usuario = get_user_model()

class DesafioTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='user_criador', password='pw'
        )
        agora = timezone.now()
        self.desafio = Desafio.objects.create(
            titulo='Desafio Python',
            descricao='Teste Python',
            tipo='DIARIO',
            categoria='PROGRAMACAO',
            criador=self.user,
            data_inicio=agora - timedelta(days=1),
            data_fim=agora + timedelta(days=1),
            ativo=True
        )

    def test_desafio_esta_ativo(self):
        """Verifica se o property esta_ativo retorna True dentro do prazo."""
        self.assertTrue(self.desafio.esta_ativo)

    def test_desafio_inativo_apos_data_fim(self):
        """Verifica se o property esta_ativo retorna False se passou a data fim."""
        self.desafio.data_fim = timezone.now() - timedelta(days=1)
        self.desafio.save()
        self.assertFalse(self.desafio.esta_ativo)
