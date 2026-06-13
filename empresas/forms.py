from django import forms
from .models import Empresa, DesafioEmpresa


class EmpresaForm(forms.ModelForm):
    """Formulário para registro e edição de empresa."""

    class Meta:
        model = Empresa
        fields = ['nome_empresa', 'cnpj', 'descricao', 'logo', 'site']
        widgets = {
            'nome_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa',
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva a empresa...',
                'rows': 4,
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'site': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.suaempresa.com.br',
            }),
        }


class DesafioEmpresaForm(forms.ModelForm):
    """Formulário para criação de desafio patrocinado por empresa."""

    class Meta:
        model = DesafioEmpresa
        fields = [
            'desafio', 'patrocinio', 'stack_avaliada', 'duracao_dias', 
            'max_candidatos', 'nivel_exigido', 'vagas_emprego', 'link_vaga',
            'metrica_consistencia', 'metrica_qualidade_ia', 'metrica_tempo', 'metrica_score'
        ]
        widgets = {
            'desafio': forms.Select(attrs={
                'class': 'form-select',
            }),
            'patrocinio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01',
                'placeholder': 'Valor do patrocínio',
            }),
            'vagas_emprego': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'link_vaga': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.suaempresa.com.br/vagas',
            }),
        }
