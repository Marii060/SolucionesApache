from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/inactivar/<int:id>/', views.inactivar_categoria, name='inactivar_categoria'),
    path('marcas/', views.lista_marcas, name='lista_marcas'),
    path('marcas/nueva/', views.crear_marca, name='crear_marca'),
    path('marcas/editar/<int:id>/', views.editar_marca, name='editar_marca'),
    path('marcas/eliminar/<int:id>/', views.eliminar_marca, name='eliminar_marca'),
    path('fabricantes/', views.lista_fabricantes, name='lista_fabricantes'),
    path('fabricantes/nuevo/', views.crear_fabricante, name='crear_fabricante'),
    path('fabricantes/editar/<int:id>/', views.editar_fabricante, name='editar_fabricante'),
    path('fabricantes/estado/<int:id>/', views.cambiar_estado_fabricante, name='cambiar_estado_fabricante'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('control/', views.control_inventario, name='control_inventario'),
    path('control/ajuste-manual/', views.ajuste_manual, name='ajuste_manual'),
    path('productos/abastecer/<int:id>/', views.abastecer_stock, name='abastecer_stock'),
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/nuevo/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/estado/<int:id>/', views.cambiar_estado_proveedor, name='cambiar_estado_proveedor'),
    path('proveedores/<int:id>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('proveedores/<int:id>/pagar/', views.registrar_pago_proveedor, name='registrar_pago_proveedor'),
        # Ruta temporal para "Nueva Compra" (Placeholder hasta que hagamos ese módulo)
    path('proveedores/<int:id>/comprar/', views.nueva_compra_placeholder, name='nueva_compra_proveedor'),
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/nueva/', views.registrar_compra, name='registrar_compra'),
    path('compras/detalle/<int:id>/', views.detalle_compra, name='detalle_compra'),
    path('compras/estado/<int:id>/', views.actualizar_estado_compra, name='actualizar_estado_compra'),
    path('compras/cancelar/<int:id>/', views.cancelar_compra, name='cancelar_compra'),
]