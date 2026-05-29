from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cliente

# Este candado asegura que nadie sin cuenta pueda entrar aquí
@login_required 
def lista_clientes(request):
    # Traemos todos los clientes de la base de datos
    clientes = Cliente.objects.all() 
    
    # Se los enviamos al HTML
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})