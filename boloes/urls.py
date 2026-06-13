from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_boloes, name='listar_boloes'),
    path('<int:pk>/', views.detalhe_bolao, name='detalhe_bolao'),
    path('criar/', views.criar_bolao, name='criar_bolao'),
    path('<int:pk>/entrar/', views.entrar_bolao, name='entrar_bolao'),
    path('<int:pk>/finalizar/', views.finalizar_bolao, name='finalizar_bolao'),
    path('<int:pk>/editar/', views.editar_bolao, name='editar_bolao'),
    path('<int:pk>/excluir/', views.excluir_bolao, name='excluir_bolao'),
]
