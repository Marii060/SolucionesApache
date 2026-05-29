from django.contrib import admin
from django.urls import path, include # <-- Importante agregar include aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conectamos las rutas de gestión
    path('gestion/', include('gestion.urls')), 
]