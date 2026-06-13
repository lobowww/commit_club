from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Empresa, DesafioEmpresa
from .forms import EmpresaForm, DesafioEmpresaForm


def empresa_required(view_func):
    """Decorator que restringe acesso a usuários com is_empresa=True."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_empresa:
            messages.error(request, 'Acesso restrito a contas de empresa.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    wrapper.__doc__ = view_func.__doc__
    return wrapper


@empresa_required
def dashboard_empresa(request):
    """
    View do dashboard da empresa.
    Exibe estatísticas e desafios patrocinados.
    """
    try:
        empresa = Empresa.objects.get(usuario=request.user)
    except Empresa.DoesNotExist:
        messages.warning(request, 'Complete o cadastro da sua empresa primeiro.')
        return redirect('registrar_empresa')

    desafios_empresa = DesafioEmpresa.objects.filter(
        empresa=empresa
    ).select_related('desafio').order_by('-data_criacao')

    context = {
        'empresa': empresa,
        'desafios_empresa': desafios_empresa,
    }
    return render(request, 'empresas/dashboard.html', context)


@empresa_required
def registrar_empresa(request):
    """View para registrar os dados da empresa."""
    # Verifica se já existe uma empresa cadastrada
    try:
        empresa = Empresa.objects.get(usuario=request.user)
        editando = True
    except Empresa.DoesNotExist:
        empresa = None
        editando = False

    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.usuario = request.user
            empresa.save()
            if editando:
                messages.success(request, 'Dados da empresa atualizados!')
            else:
                messages.success(request, 'Empresa registrada com sucesso!')
            return redirect('dashboard_empresa')
    else:
        form = EmpresaForm(instance=empresa)

    context = {
        'form': form,
        'editando': editando,
    }
    return render(request, 'empresas/registrar.html', context)


@empresa_required
def criar_desafio_empresa(request):
    """View para criar um desafio patrocinado pela empresa."""
    try:
        empresa = Empresa.objects.get(usuario=request.user)
    except Empresa.DoesNotExist:
        messages.warning(request, 'Complete o cadastro da sua empresa primeiro.')
        return redirect('registrar_empresa')

    if request.method == 'POST':
        form = DesafioEmpresaForm(request.POST)
        if form.is_valid():
            desafio_empresa = form.save(commit=False)
            desafio_empresa.empresa = empresa
            desafio_empresa.save()
            messages.success(request, 'Desafio patrocinado criado com sucesso!')
            return redirect('dashboard_empresa')
    else:
        form = DesafioEmpresaForm()

    return render(request, 'empresas/criar_desafio.html', {'form': form})
