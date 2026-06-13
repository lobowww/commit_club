from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    """Formulário de registro de novo usuário."""

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'github_username']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conte um pouco sobre você...',
                'rows': 3,
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuário do GitHub',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme a senha',
        })


class LoginForm(AuthenticationForm):
    """Formulário de login."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nome de usuário',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha',
        })


class PerfilForm(forms.ModelForm):
    """Formulário de edição de perfil do usuário."""

    class Meta:
        model = Usuario
        fields = ['bio', 'avatar', 'github_username', 'linkedin_url']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Conte um pouco sobre você...',
                'rows': 4,
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
            'github_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Usuário do GitHub',
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/seu-perfil',
            }),
        }
