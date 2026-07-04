from django.urls import path, include
from . import views

app_name = 'operaciones' 
urlpatterns = [
     #rutas para el catálogo de servicios
    path('catalogo/', views.lista_catalogo, name='lista_catalogo'),
    path('catalogo/nuevo/', views.crear_catalogo, name='crear_catalogo'),
    path('catalogo/editar/<int:id>/', views.editar_catalogo, name='editar_catalogo'),
    path('catalogo/eliminar/<int:id>/', views.eliminar_catalogo, name='eliminar_catalogo'),
    #rutas para servicios que presta el taller
    path('servicios/', views.lista_servicios, name='lista_servicios'),
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
    path('motos-cliente/<int:cliente_id>/', views.obtener_motos_cliente, name='obtener_motos_cliente'),
    path('servicios/<int:id>/', views.detalle_servicio, name='detalle_servicio'),
    path('servicios/<int:id>/estado/', views.actualizar_estado, name='actualizar_estado'),
    path('servicio/recibo/<int:servicio_id>/', views.generar_recibo, name='generar_recibo'),
    path('servicios/<int:id>/mecanico/', views.asignar_mecanico, name='asignar_mecanico'),
    #rutas para ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/nueva/', views.crear_venta, name='crear_venta'),
    path('ventas/detalle/<int:pk>/', views.detalle_venta, name='detalle_venta'),
    path('ventas/recibo/<int:pk>/', views.imprimir_recibo, name='imprimir_recibo'),
    path('ventas/anular/<int:pk>/', views.anular_venta, name='anular_venta'),
    #rutas para créditos
    path('creditos/', views.lista_creditos, name='lista_creditos'),
    path('creditos/registrar-abono/', views.registrar_abono, name='registrar_abono'),
    path('creditos/detalle/<int:credito_id>/', views.detalle_credito, name='detalle_credito'),
    #ruta AJAX que usa el buscador del formulario
    path('creditos/obtener-por-cliente/<int:cliente_id>/', views.obtener_creditos_cliente, name='obtener_creditos_cliente'),
    #rutas para reportes
    path('reportes/', views.reportes_estadisticas, name='reportes_estadisticas'),
    ]
