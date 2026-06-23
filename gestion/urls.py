from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('clientes/', views.lista_clientes, name='lista_cliente'), 
    path('clientes/nuevo/', views.crear_cliente, name='crear_cliente'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('cliente/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('cliente/eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('registrar-moto/', views.registrar_moto, name='registrar_moto'),
    path('registrar-moto/<int:id_cliente>/', views.registrar_moto, name='registrar_moto'),
    path('motos/', views.lista_motos, name='lista_motos'),
    path('moto/detalle/<int:pk>/', views.detalle_moto, name='detalle_moto'),
    path('moto/editar/<int:pk>/', views.editar_moto, name='editar_moto'),
    path('moto/eliminar/<int:pk>/', views.eliminar_moto, name='eliminar_moto'),
    path('panel/', views.panel_configuracion, name='panel'),
    path('backup/crear-manual/', views.crear_backup_manual, name='backup_crear_manual'),
]