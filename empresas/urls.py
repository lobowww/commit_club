from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_empresa, name='dashboard_empresa'),
    path('registrar/', views.registrar_empresa, name='registrar_empresa'),
    path('criar-desafio/', views.criar_desafio_empresa, name='criar_desafio_empresa'),
]
