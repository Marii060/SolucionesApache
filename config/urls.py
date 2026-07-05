from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos las rutas de gestión
    path('gestion/', include('gestion.urls')), 
    path('operaciones/', include('operaciones.urls')), 
    #ruta para el inventario
    path('inventario/', include('inventario.urls')),
]