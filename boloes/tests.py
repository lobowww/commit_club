from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from desafios.models import Desafio
from .models import Bolao, EntradaBolao

Usuario = get_user_model()

class BolaoTests(TestCase):
    def setUp(self):
        self.user1 = Usuario.objects.create_user(
            username='user1', password='pw', saldo_reais=Decimal('100.00')
        )
        self.user2 = Usuario.objects.create_user(
            username='user2', password='pw', saldo_reais=Decimal('50.00')
        )
        self.desafio = Desafio.objects.create(
            titulo='Desafio Teste',
            descricao='Teste',
            tipo='DIARIO',
            categoria='PROGRAMACAO',
            criador=self.user1,
            data_inicio=timezone.now(),
            data_fim=timezone.now() + timedelta(days=1)
        )
        self.bolao = Bolao.objects.create(
            titulo='Bolão Teste',
            descricao='Teste',
            desafio=self.desafio,
            valor_entrada=Decimal('20.00'),
            criador=self.user1,
            data_inicio=timezone.now(),
            data_fim=timezone.now() + timedelta(days=1)
        )

    def test_status_property(self):
        """Verifica se a property status e status_display retornam os valores corretos."""
        self.assertEqual(self.bolao.status, 'aberto')
        self.assertEqual(self.bolao.status_display, 'Aberto')
        
        self.bolao.ativo = False
        self.assertEqual(self.bolao.status, 'em_andamento')
        self.assertEqual(self.bolao.status_display, 'Em Andamento')
        
        self.bolao.finalizado = True
        self.assertEqual(self.bolao.status, 'finalizado')
        self.assertEqual(self.bolao.status_display, 'Finalizado')

    def test_entrada_bolao_deducao_moedas(self):
        """Simula a entrada num bolão na model layer."""
        EntradaBolao.objects.create(
            usuario=self.user1,
            bolao=self.bolao,
            valor_pago=self.bolao.valor_entrada
        )
        self.user1.saldo_reais -= self.bolao.valor_entrada
        self.user1.save()
        self.bolao.premio_total += self.bolao.valor_entrada
        self.bolao.save()

        self.assertEqual(self.user1.saldo_reais, Decimal('80.00'))
        self.assertEqual(self.bolao.premio_total, Decimal('20.00'))
        self.assertEqual(self.bolao.total_participantes, 1)
