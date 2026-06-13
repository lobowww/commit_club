from django import forms
from .models import Bolao


class BolaoForm(forms.ModelForm):
    """Formulário para criação de bolões."""

    class Meta:
        model = Bolao
        fields = [
            'titulo', 'descricao', 'desafio',
            'valor_entrada', 'regra_distribuicao', 'data_inicio', 'data_fim', 'publico'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do bolão',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva as regras do bolão...',
                'rows': 4,
            }),
            'desafio': forms.Select(attrs={
                'class': 'form-select',
            }),
            'valor_entrada': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
                'placeholder': 'Valor em moedas',
            }),
            'data_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'data_fim': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
        }
