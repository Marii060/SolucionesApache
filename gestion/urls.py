from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Esta será la ruta principal
    path('', views.dashboard, name='dashboard'), 
    
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
]