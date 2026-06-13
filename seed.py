"""
CommitClub - Seed Script
Popula o banco de dados com dados de exemplo para desenvolvimento.

Uso: python manage.py shell < seed.py
Ou:  .\venv\Scripts\python.exe manage.py shell < seed.py
"""

import os
import sys
import django
from decimal import Decimal
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commitclub.settings')
django.setup()

from django.utils import timezone
from usuarios.models import Usuario
from desafios.models import Desafio, Participacao, Comprovacao
from boloes.models import Bolao, EntradaBolao
from empresas.models import Empresa, DesafioEmpresa

print("🚀 Iniciando seed do CommitClub...")

# ─── Limpar dados existentes ───
print("🗑️  Limpando dados existentes...")
Comprovacao.objects.all().delete()
Participacao.objects.all().delete()
EntradaBolao.objects.all().delete()
Bolao.objects.all().delete()
DesafioEmpresa.objects.all().delete()
Desafio.objects.all().delete()
Empresa.objects.all().delete()
Usuario.objects.filter(is_superuser=False).delete()

# ─── Criar superusuário ───
print("👑 Criando superusuário...")
admin, created = Usuario.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@commitclub.com',
        'is_staff': True,
        'is_superuser': True,
        'bio': 'Administrador do CommitClub',
        'nivel': 10,
        'xp': 5000,
        'coins': Decimal('500.00'),
        'streak_atual': 30,
        'maior_streak': 45,
    }
)
if created:
    admin.set_password('admin123')
    admin.save()
    print("  ✅ Superusuário criado: admin / admin123")
else:
    print("  ℹ️  Superusuário já existe")

# ─── Criar usuários de teste ───
print("👥 Criando usuários de teste...")
usuarios_data = [
    {
        'username': 'maria_dev',
        'email': 'maria@example.com',
        'bio': 'Full-stack developer apaixonada por Python e React',
        'github_username': 'mariadev',
        'nivel': 5,
        'xp': 2350,
        'coins': Decimal('180.50'),
        'streak_atual': 15,
        'maior_streak': 22,
    },
    {
        'username': 'joao_data',
        'email': 'joao@example.com',
        'bio': 'Data Scientist | Machine Learning enthusiast',
        'github_username': 'joaodata',
        'nivel': 3,
        'xp': 1200,
        'coins': Decimal('95.00'),
        'streak_atual': 7,
        'maior_streak': 14,
    },
    {
        'username': 'ana_design',
        'email': 'ana@example.com',
        'bio': 'UI/UX Designer & Frontend Developer',
        'github_username': 'anadesign',
        'nivel': 4,
        'xp': 1800,
        'coins': Decimal('150.00'),
        'streak_atual': 10,
        'maior_streak': 18,
    },
    {
        'username': 'pedro_ops',
        'email': 'pedro@example.com',
        'bio': 'DevOps Engineer | Cloud Native | Kubernetes',
        'github_username': 'pedroops',
        'nivel': 6,
        'xp': 3100,
        'coins': Decimal('220.00'),
        'streak_atual': 20,
        'maior_streak': 35,
    },
    {
        'username': 'lucas_junior',
        'email': 'lucas@example.com',
        'bio': 'Estudante de Ciência da Computação - começando a jornada dev!',
        'github_username': 'lucasjr',
        'nivel': 1,
        'xp': 150,
        'coins': Decimal('15.00'),
        'streak_atual': 3,
        'maior_streak': 5,
    },
]

usuarios = []
for data in usuarios_data:
    user, created = Usuario.objects.get_or_create(
        username=data['username'],
        defaults=data
    )
    if created:
        user.set_password('teste123')
        user.save()
    usuarios.append(user)
    print(f"  {'✅' if created else 'ℹ️'} {data['username']}")

# ─── Criar empresa ───
print("🏢 Criando empresa de teste...")
empresa_user, created = Usuario.objects.get_or_create(
    username='techcorp',
    defaults={
        'email': 'contato@techcorp.com',
        'bio': 'TechCorp - Soluções em tecnologia',
        'is_empresa': True,
        'nivel': 1,
        'xp': 0,
        'coins': Decimal('1000.00'),
    }
)
if created:
    empresa_user.set_password('empresa123')
    empresa_user.save()

empresa, created = Empresa.objects.get_or_create(
    usuario=empresa_user,
    defaults={
        'nome_empresa': 'TechCorp Brasil',
        'cnpj': '12.345.678/0001-90',
        'descricao': 'Empresa líder em soluções de tecnologia e inovação.',
        'site': 'https://techcorp.com.br',
    }
)
print(f"  {'✅' if created else 'ℹ️'} TechCorp Brasil")

# ─── Criar desafios ───
print("🎯 Criando desafios...")
now = timezone.now()

desafios_data = [
    {
        'titulo': '30 Dias de Python',
        'descricao': 'Domine Python em 30 dias! Resolva um desafio por dia, desde conceitos básicos até projetos avançados com Django e FastAPI.',
        'tipo': 'MENSAL',
        'categoria': 'PROGRAMACAO',
        'criador': usuarios[0],
        'data_inicio': now - timedelta(days=5),
        'data_fim': now + timedelta(days=25),
        'max_participantes': 100,
        'xp_recompensa': 300,
        'coins_recompensa': Decimal('50.00'),
    },
    {
        'titulo': 'Semana do React',
        'descricao': 'Uma semana intensiva de React! Construa componentes, hooks customizados e um projeto completo com Next.js.',
        'tipo': 'SEMANAL',
        'categoria': 'PROGRAMACAO',
        'criador': usuarios[2],
        'data_inicio': now,
        'data_fim': now + timedelta(days=7),
        'max_participantes': 50,
        'xp_recompensa': 150,
        'coins_recompensa': Decimal('25.00'),
    },
    {
        'titulo': 'Design System Challenge',
        'descricao': 'Crie um Design System completo do zero! Inclui tipografia, cores, componentes e documentação no Figma.',
        'tipo': 'SEMANAL',
        'categoria': 'DESIGN',
        'criador': usuarios[2],
        'data_inicio': now - timedelta(days=2),
        'data_fim': now + timedelta(days=5),
        'max_participantes': 30,
        'xp_recompensa': 200,
        'coins_recompensa': Decimal('30.00'),
    },
    {
        'titulo': 'Machine Learning do Zero',
        'descricao': 'Aprenda ML na prática! Do pré-processamento à produção. Inclui projetos com scikit-learn, TensorFlow e deploy.',
        'tipo': 'MENSAL',
        'categoria': 'DADOS',
        'criador': usuarios[1],
        'data_inicio': now,
        'data_fim': now + timedelta(days=30),
        'max_participantes': 40,
        'xp_recompensa': 500,
        'coins_recompensa': Decimal('80.00'),
    },
    {
        'titulo': 'Docker & Kubernetes Bootcamp',
        'descricao': 'Domine containerização! De Dockerfile básico a clusters Kubernetes em produção.',
        'tipo': 'SEMANAL',
        'categoria': 'DEVOPS',
        'criador': usuarios[3],
        'data_inicio': now + timedelta(days=1),
        'data_fim': now + timedelta(days=8),
        'max_participantes': 25,
        'xp_recompensa': 200,
        'coins_recompensa': Decimal('35.00'),
    },
    {
        'titulo': 'Commit Diário - 7 dias',
        'descricao': 'Faça pelo menos 1 commit por dia durante 7 dias seguidos. Qualquer projeto conta!',
        'tipo': 'DIARIO',
        'categoria': 'PROGRAMACAO',
        'criador': admin,
        'data_inicio': now,
        'data_fim': now + timedelta(days=7),
        'max_participantes': 200,
        'xp_recompensa': 100,
        'coins_recompensa': Decimal('15.00'),
    },
    {
        'titulo': 'Estudar SQL Avançado',
        'descricao': 'Window functions, CTEs, otimização de queries e modelagem de dados. Resolva 20 exercícios progressivos.',
        'tipo': 'SEMANAL',
        'categoria': 'DADOS',
        'criador': usuarios[1],
        'data_inicio': now - timedelta(days=1),
        'data_fim': now + timedelta(days=6),
        'max_participantes': 60,
        'xp_recompensa': 120,
        'coins_recompensa': Decimal('20.00'),
    },
    {
        'titulo': 'API REST com FastAPI',
        'descricao': 'Construa uma API REST completa com FastAPI, autenticação JWT, testes e documentação Swagger.',
        'tipo': 'SEMANAL',
        'categoria': 'PROGRAMACAO',
        'criador': usuarios[0],
        'data_inicio': now + timedelta(days=3),
        'data_fim': now + timedelta(days=10),
        'max_participantes': 35,
        'xp_recompensa': 180,
        'coins_recompensa': Decimal('28.00'),
    },
]

desafios = []
for data in desafios_data:
    desafio = Desafio.objects.create(**data)
    desafios.append(desafio)
    print(f"  ✅ {data['titulo']}")

# ─── Criar participações ───
print("📝 Criando participações...")
participacoes_data = [
    (usuarios[0], desafios[3], 45, False),
    (usuarios[0], desafios[5], 70, False),
    (usuarios[1], desafios[0], 30, False),
    (usuarios[1], desafios[6], 60, False),
    (usuarios[2], desafios[0], 20, False),
    (usuarios[2], desafios[1], 50, False),
    (usuarios[3], desafios[4], 80, False),
    (usuarios[3], desafios[5], 100, True),
    (usuarios[4], desafios[0], 10, False),
    (usuarios[4], desafios[5], 40, False),
    (usuarios[4], desafios[1], 15, False),
]

participacoes = []
for user, desafio, progresso, concluido in participacoes_data:
    part = Participacao.objects.create(
        usuario=user,
        desafio=desafio,
        progresso=progresso,
        concluido=concluido
    )
    participacoes.append(part)
    print(f"  ✅ {user.username} → {desafio.titulo} ({progresso}%)")

# ─── Criar comprovações ───
print("📎 Criando comprovações...")
comprovacoes_data = [
    (participacoes[0], 'Completei o módulo de regressão linear com scikit-learn', True),
    (participacoes[2], 'Resolvi 10 exercícios de Python no LeetCode', True),
    (participacoes[5], 'Criei 3 componentes React com hooks customizados', None),
    (participacoes[6], 'Deploy de aplicação com Docker Compose funcionando', True),
    (participacoes[7], 'Todos os commits do desafio estão no GitHub', True),
]

for part, desc, aprovada in comprovacoes_data:
    Comprovacao.objects.create(
        participacao=part,
        descricao=desc,
        link='https://github.com/exemplo/projeto',
        aprovada=aprovada
    )
    print(f"  ✅ Comprovação para {part.usuario.username}")

# ─── Criar bolões ───
print("🎰 Criando bolões...")
boloes_data = [
    {
        'titulo': 'Bolão - 30 Dias de Python',
        'descricao': 'Quem completa mais tarefas no desafio de Python em 30 dias leva o prêmio!',
        'desafio': desafios[0],
        'valor_entrada': Decimal('10.00'),
        'premio_total': Decimal('50.00'),
        'criador': usuarios[0],
        'data_inicio': now,
        'data_fim': now + timedelta(days=25),
    },
    {
        'titulo': 'Bolão Semanal - Commits',
        'descricao': 'Quem fizer mais commits durante a semana ganha! Mínimo 1 commit por dia.',
        'desafio': desafios[5],
        'valor_entrada': Decimal('5.00'),
        'premio_total': Decimal('25.00'),
        'criador': admin,
        'data_inicio': now,
        'data_fim': now + timedelta(days=7),
    },
    {
        'titulo': 'Bolão ML Master',
        'descricao': 'Competição de Machine Learning! Complete o roadmap e apresente seu projeto final.',
        'desafio': desafios[3],
        'valor_entrada': Decimal('20.00'),
        'premio_total': Decimal('100.00'),
        'criador': usuarios[1],
        'data_inicio': now,
        'data_fim': now + timedelta(days=30),
    },
]

boloes = []
for data in boloes_data:
    bolao = Bolao.objects.create(**data)
    boloes.append(bolao)
    print(f"  ✅ {data['titulo']}")

# ─── Criar entradas nos bolões ───
print("🎟️  Criando entradas nos bolões...")
entradas_data = [
    (usuarios[0], boloes[0], Decimal('10.00')),
    (usuarios[1], boloes[0], Decimal('10.00')),
    (usuarios[2], boloes[0], Decimal('10.00')),
    (usuarios[4], boloes[0], Decimal('10.00')),
    (usuarios[3], boloes[1], Decimal('5.00')),
    (usuarios[4], boloes[1], Decimal('5.00')),
    (usuarios[0], boloes[2], Decimal('20.00')),
    (usuarios[1], boloes[2], Decimal('20.00')),
]

for user, bolao, valor in entradas_data:
    EntradaBolao.objects.create(
        usuario=user,
        bolao=bolao,
        valor_pago=valor
    )
    # Atualizar prêmio total
    bolao.premio_total += valor
    bolao.save()
    print(f"  ✅ {user.username} → {bolao.titulo}")

# ─── Criar desafio de empresa ───
print("🏢 Criando desafio patrocinado...")
DesafioEmpresa.objects.create(
    empresa=empresa,
    desafio=desafios[0],
    patrocinio=Decimal('500.00'),
    vagas_emprego=True,
    link_vaga='https://techcorp.com.br/vagas/python-developer'
)
print("  ✅ TechCorp → 30 Dias de Python")

print()
print("=" * 50)
print("🎉 Seed concluído com sucesso!")
print("=" * 50)
print(f"  👥 {Usuario.objects.count()} usuários")
print(f"  🎯 {Desafio.objects.count()} desafios")
print(f"  📝 {Participacao.objects.count()} participações")
print(f"  📎 {Comprovacao.objects.count()} comprovações")
print(f"  🎰 {Bolao.objects.count()} bolões")
print(f"  🎟️  {EntradaBolao.objects.count()} entradas em bolões")
print(f"  🏢 {Empresa.objects.count()} empresas")
print(f"  🏷️  {DesafioEmpresa.objects.count()} desafios patrocinados")
print()
print("🔑 Credenciais de teste:")
print("  Admin: admin / admin123")
print("  Usuários: maria_dev, joao_data, ana_design, pedro_ops, lucas_junior / teste123")
print("  Empresa: techcorp / empresa123")
