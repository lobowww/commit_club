from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),
    path('carteira/', views.carteira, name='carteira'),
    path('adicionar-saldo/', views.adicionar_saldo, name='adicionar_saldo'),
    path('concluir-onboarding/', views.concluir_onboarding, name='concluir_onboarding'),
]
