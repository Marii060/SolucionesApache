from django.contrib import admin
from .models import Cliente, Moto, Rol, Log

# Esto permite que al abrir un cliente, veas y agregues sus motos ahí mismo.
class MotoInline(admin.TabularInline):
    model = Moto
    extra = 1 # Muestra una fila en blanco lista para agregar una moto

# 2. SECCIÓN DE CLIENTES
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Qué columnas queremos ver en la lista principal
    list_display = ('numero_documento', 'razon_social', 'nombre', 'correo', 'telefono')
    
    # Barra de búsqueda (puedes buscar por cédula, nombre, etc.)
    search_fields = ('numero_documento', 'razon_social', 'nombre', 'correo')
    
    # Le conectamos el "Inline" de las motos
    inlines = [MotoInline]

# 3. SECCIÓN DE MOTOS (Vista Individual)
# Por si quieres ver el listado de TODAS las motos del taller
@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'cilindraje', 'id_cliente')
    list_filter = ('marca',) # Filtro lateral para buscar por marca (Yamaha, Honda, etc.)
    
    # Permite buscar la placa de la moto o el nombre de su dueño
    search_fields = ('placa', 'id_cliente__razon_social', 'id_cliente__nombre')
    
@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id_rol', 'nombre')
    search_fields = ('nombre',)

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    # Mostramos a qué hora, quién y qué hizo
    list_display = ('fecha_hora', 'id_usuario', 'accion_realizada')
    list_filter = ('fecha_hora', 'id_usuario')
    search_fields = ('accion_realizada', 'id_usuario__username', 'descripcion')    