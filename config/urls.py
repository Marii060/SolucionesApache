from django.contrib import admin
from django.urls import path, include # <-- Importante agregar include aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aquí activamos todo el sistema de Login/Logout seguro de Django
    path('cuentas/', include('django.contrib.auth.urls')),
    # Conectamos las rutas de gestión
    path('gestion/', include('gestion.urls')), 
]