from django.contrib import admin
from .models import ListaServicio, Servicio, DetalleServicio

#Permite agregar los repuestos y trabajos directamente dentro de la orden de servicio
class DetalleServicioInline(admin.TabularInline):
    model = DetalleServicio
    extra = 1  # Muestra una línea vacía por defecto para agregar datos
    db_column = 'id_servicio'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    # Columnas que se verán en la lista general de servicios
    list_display = ('codigo_servicio', 'id_moto', 'id_usuario', 'estado', 'fecha_inicio', 'valor_total')
    
    # Filtros laterales para buscar más rápido
    list_filter = ('estado', 'fecha_inicio')
    
    # Buscador por placa de moto o código de servicio
    search_fields = ('codigo_servicio', 'id_moto__placa')
    
    # Metemos el inline para cargar los detalles en la misma pantalla
    inlines = [DetalleServicioInline]

# Registro del catálogo de servicios disponibles (Mano de obra base)
@admin.register(ListaServicio)
class ListaServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'precio_base_mano_obra', 'estado')
    search_fields = ('nombre_servicio',)
