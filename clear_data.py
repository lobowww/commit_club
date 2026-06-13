import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'commitclub.settings')
django.setup()

from desafios.models import Desafio
from boloes.models import Bolao

print(f"Limpando bolões... {Bolao.objects.count()} excluidos.")
Bolao.objects.all().delete()

print(f"Limpando desafios... {Desafio.objects.count()} excluidos.")
Desafio.objects.all().delete()

print("Base limpa!")
