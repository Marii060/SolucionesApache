from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/inactivar/<int:id>/', views.inactivar_categoria, name='inactivar_categoria'),
    path('marcas/', views.lista_marcas, name='lista_marcas'),
    path('marcas/nueva/', views.crear_marca, name='crear_marca'),
    path('marcas/editar/<int:id>/', views.editar_marca, name='editar_marca'),
    path('marcas/eliminar/<int:id>/', views.eliminar_marca, name='eliminar_marca'),
]