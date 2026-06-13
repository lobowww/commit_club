from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Bolao, EntradaBolao, Premiacao
from .forms import BolaoForm


@login_required
def listar_boloes(request):
    """View para listar todos os bolões ativos."""
    boloes = Bolao.objects.filter(
        ativo=True, finalizado=False, publico=True
    ).order_by('-data_criacao')

    context = {'boloes': boloes}
    return render(request, 'boloes/listar.html', context)


@login_required
def detalhe_bolao(request, pk):
    """
    View de detalhe de um bolão.
    Exibe informações, participantes e premiações.
    """
    bolao = get_object_or_404(Bolao, pk=pk)
    entradas = bolao.entradas.select_related('usuario').all()
    premiacoes = bolao.premiacoes.select_related('usuario').order_by('posicao')

    # Verifica se o usuário já entrou no bolão
    ja_entrou = EntradaBolao.objects.filter(
        usuario=request.user, bolao=bolao
    ).exists()

    context = {
        'bolao': bolao,
        'entradas': entradas,
        'premiacoes': premiacoes,
        'ja_entrou': ja_entrou,
    }
    return render(request, 'boloes/detalhe.html', context)


@login_required
def criar_bolao(request):
    """View para criação de um novo bolão."""
    if request.method == 'POST':
        form = BolaoForm(request.POST)
        if form.is_valid():
            bolao = form.save(commit=False)
            bolao.criador = request.user
            bolao.save()
            messages.success(request, 'Bolão criado com sucesso!')
            return redirect('detalhe_bolao', pk=bolao.pk)
    else:
        form = BolaoForm()

    return render(request, 'boloes/criar.html', {'form': form})


@login_required
def entrar_bolao(request, pk):
    """
    View para entrar em um bolão.
    Deduz o valor de entrada das moedas do usuário.
    """
    bolao = get_object_or_404(Bolao, pk=pk)
    usuario = request.user

    # Validações
    if bolao.finalizado:
        messages.error(request, 'Este bolão já foi finalizado.')
        return redirect('detalhe_bolao', pk=pk)

    if not bolao.ativo:
        messages.error(request, 'Este bolão não está mais ativo.')
        return redirect('detalhe_bolao', pk=pk)

    if EntradaBolao.objects.filter(usuario=usuario, bolao=bolao).exists():
        messages.warning(request, 'Você já está participando deste bolão.')
        return redirect('detalhe_bolao', pk=pk)

    # Verifica saldo de reais
    if usuario.saldo_reais < bolao.valor_entrada:
        messages.error(
            request,
            f'Saldo insuficiente! Você tem R$ {usuario.saldo_reais}, '
            f'mas precisa de R$ {bolao.valor_entrada}.'
        )
        return redirect('detalhe_bolao', pk=pk)

    # Deduzir saldo e criar entrada
    usuario.saldo_reais -= bolao.valor_entrada
    usuario.save()

    EntradaBolao.objects.create(
        usuario=usuario,
        bolao=bolao,
        valor_pago=bolao.valor_entrada,
    )

    # Atualizar prêmio total do bolão
    bolao.premio_total += bolao.valor_entrada
    bolao.save()

    messages.success(
        request,
        f'Você entrou no bolão "{bolao.titulo}"! '
        f'R$ {bolao.valor_entrada} foram descontados do seu saldo.'
    )
    return redirect('detalhe_bolao', pk=pk)


@login_required
def finalizar_bolao(request, pk):
    """
    View para finalizar um bolão e distribuir os prêmios.
    Apenas o criador do bolão pode finalizá-lo.
    Distribuição: 1º lugar = 50%, 2º lugar = 30%, 3º lugar = 20%.
    """
    bolao = get_object_or_404(Bolao, pk=pk)

    # Apenas o criador pode finalizar
    if bolao.criador != request.user:
        messages.error(request, 'Apenas o criador pode finalizar o bolão.')
        return redirect('detalhe_bolao', pk=pk)

    if bolao.finalizado:
        messages.warning(request, 'Este bolão já foi finalizado.')
        return redirect('detalhe_bolao', pk=pk)

    entradas = bolao.entradas.select_related('usuario').all()

    if entradas.count() < 1:
        messages.error(request, 'O bolão precisa ter pelo menos 1 participante.')
        return redirect('detalhe_bolao', pk=pk)

    # Distribuição de prêmios
    premio_total = bolao.premio_total
    participantes = list(entradas)

    if bolao.regra_distribuicao == 'WINNER':
        distribuicao = [Decimal('1.00')]
    else:
        distribuicao = [Decimal('0.50'), Decimal('0.30'), Decimal('0.20')]

    for i, entrada in enumerate(participantes[:len(distribuicao)]):
        valor_premio = premio_total * distribuicao[i]
        Premiacao.objects.create(
            bolao=bolao,
            usuario=entrada.usuario,
            valor=valor_premio,
            posicao=i + 1,
        )
        # Creditar saldo ao vencedor
        entrada.usuario.saldo_reais += valor_premio
        entrada.usuario.save()

    # Marcar bolão como finalizado
    bolao.finalizado = True
    bolao.ativo = False
    bolao.save()

    messages.success(request, f'Bolão "{bolao.titulo}" finalizado! Prêmios distribuídos.')
    return redirect('detalhe_bolao', pk=pk)


@login_required
def editar_bolao(request, pk):
    bolao = get_object_or_404(Bolao, pk=pk, criador=request.user)
    if bolao.entradas.count() > 0:
        messages.error(request, 'Não é possível editar um bolão que já tem participantes.')
        return redirect('detalhe_bolao', pk=pk)
        
    if request.method == 'POST':
        form = BolaoForm(request.POST, instance=bolao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bolão atualizado com sucesso!')
            return redirect('detalhe_bolao', pk=bolao.pk)
    else:
        form = BolaoForm(instance=bolao)
    return render(request, 'boloes/criar.html', {'form': form, 'editando': True})


@login_required
def excluir_bolao(request, pk):
    bolao = get_object_or_404(Bolao, pk=pk, criador=request.user)
    if request.method == 'POST':
        bolao.delete()
        messages.success(request, 'Bolão excluído com sucesso!')
        return redirect('listar_boloes')
    return render(request, 'boloes/excluir.html', {'bolao': bolao})
