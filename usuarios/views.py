from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistroForm, LoginForm, PerfilForm
from .models import Usuario


def registro(request):
    """View para registro de novo usuário."""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.saldo_reais = Decimal('50.00')
            user.save()
            messages.success(request, 'Conta criada com sucesso! Você ganhou R$ 50,00 para começar. Faça login para continuar.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    """View para login de usuário."""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciais inválidas.')
        else:
            messages.error(request, 'Credenciais inválidas.')
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    """View para logout de usuário."""
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('home')


@login_required
def dashboard(request):
    """
    View do dashboard do usuário.
    Exibe estatísticas: desafios ativos, XP, moedas, streak, nível.
    """
    usuario = request.user

    # Importações lazy para evitar dependências circulares
    try:
        from desafios.models import Participacao
        desafios_ativos = Participacao.objects.filter(
            usuario=usuario, concluido=False
        ).select_related('desafio').count()
        participacoes_recentes = Participacao.objects.filter(
            usuario=usuario
        ).select_related('desafio').order_by('-data_entrada')[:5]
    except ImportError:
        desafios_ativos = 0
        participacoes_recentes = []

    try:
        from boloes.models import EntradaBolao
        boloes_ativos = EntradaBolao.objects.filter(
            usuario=usuario, bolao__finalizado=False
        ).count()
    except ImportError:
        boloes_ativos = 0

    context = {
        'usuario': usuario,
        'desafios_ativos': desafios_ativos,
        'participacoes_recentes': participacoes_recentes,
        'boloes_ativos': boloes_ativos,
    }
    return render(request, 'usuarios/dashboard.html', context)


@login_required
def perfil(request):
    """View para visualização e edição do perfil do usuário."""
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'usuarios/perfil.html', {'form': form})


@login_required
def carteira(request):
    """
    View da carteira virtual do usuário.
    Exibe saldo de moedas e histórico de transações (premiações).
    """
    usuario = request.user

    # Histórico de premiações recebidas
    try:
        from boloes.models import Premiacao
        premiacoes = Premiacao.objects.filter(
            usuario=usuario
        ).select_related('bolao').order_by('-data_premiacao')
    except ImportError:
        premiacoes = []

    # Histórico de entradas em bolões (gastos)
    try:
        from boloes.models import EntradaBolao
        entradas = EntradaBolao.objects.filter(
            usuario=usuario
        ).select_related('bolao').order_by('-data_entrada')
    except ImportError:
        entradas = []

    context = {
        'usuario': usuario,
        'premiacoes': premiacoes,
        'entradas': entradas,
    }
    return render(request, 'usuarios/carteira.html', context)


@login_required
def adicionar_saldo(request):
    if request.method == 'POST':
        try:
            valor_str = request.POST.get('valor', '0').replace(',', '.')
            valor = float(valor_str)
            if valor > 0:
                request.user.saldo_reais += Decimal(str(valor))
                request.user.save()
                messages.success(request, f'R$ {valor:.2f} adicionados à sua carteira com sucesso!')
            else:
                messages.error(request, 'Valor inválido.')
        except ValueError:
            messages.error(request, 'Valor inválido.')
            
    return redirect('carteira')


from django.http import JsonResponse
import json

@login_required
def concluir_onboarding(request):
    """Marca o onboarding do usuário como completo via API/Fetch."""
    if request.method == 'POST':
        request.user.onboarding_completo = True
        request.user.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
