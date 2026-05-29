from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Cuando visiten /clientes/, Django ejecutará la vista lista_clientes
    path('clientes/', views.lista_clientes, name='lista_clientes'),
]