from django.urls import path, include
from . import views

app_name = 'operaciones' # Esto es clave para que Django sepa de qué app es la URL

urlpatterns = [
    # Ruta para la pantalla que acabamos de crear
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
]