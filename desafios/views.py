from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

from .models import Desafio, Participacao, Comprovacao
from .forms import DesafioForm, ComprovacaoForm


def explorar(request):
    """
    View para listar todos os desafios ativos.
    Suporta busca por texto e filtro por categoria.
    """
    desafios = Desafio.objects.filter(ativo=True, publico=True, data_fim__gte=timezone.now())

    # Filtro por busca textual
    busca = request.GET.get('busca', '')
    if busca:
        desafios = desafios.filter(
            Q(titulo__icontains=busca) | Q(descricao__icontains=busca)
        )

    # Filtro por categoria
    categoria = request.GET.get('categoria', '').upper()
    if categoria:
        desafios = desafios.filter(categoria=categoria)

    context = {
        'desafios': desafios,
        'busca': busca,
        'categoria_selecionada': categoria.lower(),
        'categorias': Desafio.CATEGORIA_CHOICES,
    }
    return render(request, 'desafios/explorar.html', context)


def detalhe_desafio(request, pk):
    """
    View de detalhe de um desafio.
    Exibe informações, participantes e permite entrar no desafio.
    """
    desafio = get_object_or_404(Desafio, pk=pk)
    
    # Gera o roadmap via IA se não existir
    if not desafio.roadmap_ia:
        from gemini_utils import gerar_roadmap_desafio
        duracao = (desafio.data_fim - desafio.data_inicio).days or 1
        roadmap = gerar_roadmap_desafio(desafio.titulo, duracao)
        if roadmap:
            desafio.roadmap_ia = roadmap
            desafio.save()

    participacoes = desafio.participacoes.select_related('usuario').all()

    # Verifica se o usuário logado já participa
    ja_participa = False
    participacao_usuario = None
    if request.user.is_authenticated:
        try:
            participacao_usuario = Participacao.objects.get(
                usuario=request.user, desafio=desafio
            )
            ja_participa = True
        except Participacao.DoesNotExist:
            pass

    context = {
        'desafio': desafio,
        'participacoes': participacoes,
        'ja_participa': ja_participa,
        'participacao_usuario': participacao_usuario,
    }
    return render(request, 'desafios/detalhe.html', context)


@login_required
def criar_desafio(request):
    """View para criação de um novo desafio."""
    if request.method == 'POST':
        form = DesafioForm(request.POST, request.FILES)
        if form.is_valid():
            desafio = form.save(commit=False)
            desafio.criador = request.user
            desafio.save()
            messages.success(request, 'Desafio criado com sucesso!')
            return redirect('detalhe_desafio', pk=desafio.pk)
    else:
        form = DesafioForm()

    return render(request, 'desafios/criar.html', {'form': form})


@login_required
def participar(request, pk):
    """View para participar de um desafio."""
    desafio = get_object_or_404(Desafio, pk=pk)

    # Validações
    if not desafio.esta_ativo:
        messages.error(request, 'Este desafio não está mais ativo.')
        return redirect('detalhe_desafio', pk=pk)

    if desafio.total_participantes >= desafio.max_participantes:
        messages.error(request, 'Este desafio já atingiu o número máximo de participantes.')
        return redirect('detalhe_desafio', pk=pk)

    # Verifica se já participa
    if Participacao.objects.filter(usuario=request.user, desafio=desafio).exists():
        messages.warning(request, 'Você já está participando deste desafio.')
        return redirect('detalhe_desafio', pk=pk)

    # Criar participação
    Participacao.objects.create(usuario=request.user, desafio=desafio)
    messages.success(request, f'Você entrou no desafio "{desafio.titulo}"!')
    return redirect('detalhe_desafio', pk=pk)


@login_required
def enviar_comprovacao(request, pk):
    """View para enviar comprovação de progresso em um desafio."""
    desafio = get_object_or_404(Desafio, pk=pk)

    try:
        participacao = Participacao.objects.get(
            usuario=request.user, desafio=desafio
        )
    except Participacao.DoesNotExist:
        messages.error(request, 'Você não está participando deste desafio.')
        return redirect('detalhe_desafio', pk=pk)

    if request.method == 'POST':
        form = ComprovacaoForm(request.POST, request.FILES)
        if form.is_valid():
            comprovacao = form.save(commit=False)
            comprovacao.participacao = participacao
            comprovacao.save()
            messages.success(request, 'Comprovação enviada com sucesso! Aguarde aprovação.')
            return redirect('detalhe_desafio', pk=pk)
    else:
        form = ComprovacaoForm()

    context = {
        'form': form,
        'desafio': desafio,
        'participacao': participacao,
    }
    return render(request, 'desafios/comprovar.html', context)


@login_required
def meus_desafios(request):
    """View para listar os desafios do usuário (criados e participando)."""
    participacoes = Participacao.objects.filter(
        usuario=request.user
    ).select_related('desafio').order_by('-data_entrada')

    desafios_criados = Desafio.objects.filter(
        criador=request.user
    ).order_by('-data_criacao')

    context = {
        'participacoes': participacoes,
        'desafios_criados': desafios_criados,
    }
    return render(request, 'desafios/meus_desafios.html', context)


@login_required
def editar_desafio(request, pk):
    desafio = get_object_or_404(Desafio, pk=pk, criador=request.user)
    if request.method == 'POST':
        form = DesafioForm(request.POST, request.FILES, instance=desafio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Desafio atualizado com sucesso!')
            return redirect('detalhe_desafio', pk=desafio.pk)
    else:
        form = DesafioForm(instance=desafio)
    return render(request, 'desafios/criar.html', {'form': form, 'editando': True})


@login_required
def excluir_desafio(request, pk):
    desafio = get_object_or_404(Desafio, pk=pk, criador=request.user)
    if request.method == 'POST':
        desafio.delete()
        messages.success(request, 'Desafio excluído com sucesso!')
        return redirect('meus_desafios')
    return render(request, 'desafios/excluir.html', {'desafio': desafio})
