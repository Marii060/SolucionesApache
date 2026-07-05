from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', RedirectView.as_view(url='/gestion/login/', permanent=False), name='login'),
    # Conectamos las rutas de gestión
    path('gestion/', include('gestion.urls')), 
    path('operaciones/', include('operaciones.urls')), 
    #ruta para el inventario
    path('inventario/', include('inventario.urls')),
]