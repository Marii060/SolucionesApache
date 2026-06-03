from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('clientes/', views.lista_clientes, name='lista_clientes'), 
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]