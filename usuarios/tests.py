from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

Usuario = get_user_model()

class GamificacaoTests(TestCase):
    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='testuser',
            password='password123',
            nivel=1,
            xp=0,
            saldo_reais=Decimal('0.00')
        )

    def test_adicionar_xp_sem_subir_nivel(self):
        """Testa se a adição de XP atualiza XP corretamente sem subir de nível."""
        self.user.adicionar_xp(50)
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp, 50)
        self.assertEqual(self.user.nivel, 1)

    def test_adicionar_xp_subindo_nivel(self):
        """Testa se a adição de XP suficiente faz o usuário subir de nível."""
        self.user.adicionar_xp(120)
        self.user.refresh_from_db()
        # Nível 1 precisa de 100 XP para passar pro Nível 2
        self.assertEqual(self.user.nivel, 2)
        self.assertEqual(self.user.xp, 20) # 120 - 100

    def test_progresso_nivel_property(self):
        """Verifica se a property progresso_nivel funciona."""
        self.user.xp = 45
        self.assertEqual(self.user.progresso_nivel, 45)
