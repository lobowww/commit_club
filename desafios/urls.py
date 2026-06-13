from django.urls import path
from . import views

urlpatterns = [
    path('explorar/', views.explorar, name='explorar_desafios'),
    path('<int:pk>/', views.detalhe_desafio, name='detalhe_desafio'),
    path('criar/', views.criar_desafio, name='criar_desafio'),
    path('<int:pk>/participar/', views.participar, name='participar'),
    path('<int:pk>/comprovar/', views.enviar_comprovacao, name='enviar_comprovacao'),
    path('meus/', views.meus_desafios, name='meus_desafios'),
    path('<int:pk>/editar/', views.editar_desafio, name='editar_desafio'),
    path('<int:pk>/excluir/', views.excluir_desafio, name='excluir_desafio'),
]
