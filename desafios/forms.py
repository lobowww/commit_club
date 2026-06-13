from django import forms
from .models import Desafio, Comprovacao


class DesafioForm(forms.ModelForm):
    """Formulário para criação e edição de desafios."""

    class Meta:
        model = Desafio
        fields = [
            'titulo', 'descricao', 'tipo', 'categoria',
            'data_inicio', 'data_fim', 'max_participantes',
            'xp_recompensa', 'coins_recompensa', 'imagem', 'publico'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do desafio',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva o desafio em detalhes...',
                'rows': 5,
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            'data_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'data_fim': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'max_participantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
            'xp_recompensa': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
            'coins_recompensa': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }


class ComprovacaoForm(forms.ModelForm):
    """Formulário para envio de comprovação de progresso."""

    class Meta:
        model = Comprovacao
        fields = ['descricao', 'arquivo', 'link']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva o que você fez...',
                'rows': 4,
            }),
            'arquivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/seu-repo/commit/...',
            }),
        }
