from django.urls import path, include
from . import views

app_name = 'operaciones' # Esto es clave para que Django sepa de qué app es la URL

urlpatterns = [
     #rutas para el catálogo de servicios
    path('catalogo/', views.lista_catalogo, name='lista_catalogo'),
    path('catalogo/nuevo/', views.crear_catalogo, name='crear_catalogo'),
    path('catalogo/editar/<int:id>/', views.editar_catalogo, name='editar_catalogo'),
    path('catalogo/eliminar/<int:id>/', views.eliminar_catalogo, name='eliminar_catalogo'),
    #rutas para servicios que presta el taller
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
]