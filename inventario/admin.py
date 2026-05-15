from django.contrib import admin
from .models import MarcaProducto, Categoria, Proveedor, Producto

@admin.register(MarcaProducto)
class MarcaProductoAdmin(admin.ModelAdmin):
    list_display = ('id_marca', 'nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo_interno', 'nombre', 'estado', 'fecha_creacion')
    list_filter = ('estado',)
    search_fields = ('nombre', 'codigo_interno')

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'identificacion', 'telefono', 'correo', 'activo')
    list_filter = ('activo',)
    search_fields = ('razon_social', 'identificacion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Mostramos los campos principales incluyendo stock y precios
    list_display = ('codigo_interno', 'nombre', 'id_categoria', 'precio_venta', 'cantidad', 'disponible')
    # Filtros laterales por categoría, marca y disponibilidad
    list_filter = ('id_categoria', 'id_marca', 'disponible')
    # Buscador por nombre y códigos
    search_fields = ('nombre', 'codigo_interno', 'codigo_barras')
    # Esto permite seleccionar los proveedores de forma más cómoda en la relación Muchos a Muchos
    filter_horizontal = ('proveedores',)