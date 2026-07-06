from django.contrib import admin
from .models import ListaServicio, Servicio, DetalleServicio, Venta, DetalleVenta, Credito, CreditoPagado

#Permite agregar los repuestos y trabajos directamente dentro de la orden de servicio
class DetalleServicioInline(admin.TabularInline):
    model = DetalleServicio
    extra = 1  # Muestra una línea vacía por defecto para agregar datos
    db_column = 'id_servicio'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    # Columnas que se verán en la lista general de servicios
    list_display = ('codigo_servicio', 'id_moto', 'id_usuario', 'estado', 'mecanico', 'fecha_inicio', 'valor_total')
    
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

# Esto permite agregar los productos directamente dentro de la factura de venta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('num_factura', 'id_cliente', 'fecha_venta', 'total_venta', 'tipo_pago')
    list_filter = ('fecha_venta', 'tipo_pago')
    search_fields = ('num_factura', 'id_cliente__razon_social', 'id_cliente__nombre')
    inlines = [DetalleVentaInline]

@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'valor_total', 'saldo_pendiente', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('cliente__nombre',) 

@admin.register(CreditoPagado)
class CreditoPagadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'credito', 'monto_pago', 'saldo_restante', 'metodo_pago', 'fecha_pago', 'usuario')
    list_filter = ('metodo_pago', 'fecha_pago')
    # Creamos la columna personalizada que va y busca el saldo en la tabla de Crédito
    def saldo_restante(self, obj):
        if obj.credito:
            return f"$ {obj.credito.saldo_pendiente}"
        return "Sin asignar"
    # Le ponemos un nombre bonito a la cabecera de la columna
    saldo_restante.short_description = 'Saldo Pendiente'