from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cliente, Moto # Perfecto, aquí tienes los modelos

@login_required
def dashboard(request):
    # Va a la DB y cuenta cuántos clientes hay
    total_clientes = Cliente.objects.count()
    
    # Va a la DB y cuenta cuántas motos hay
    total_motos = Moto.objects.count() 
    
    contexto = {
        'total_clientes': total_clientes,
        'total_motos': total_motos,
    }
    # Renderizamos la pantalla enviando el contexto de la base de datos
    return render(request, 'gestion/dashboard.html', contexto)

@login_required 
def lista_clientes(request):
    # Traemos todos los clientes de la base de datos
    clientes = Cliente.objects.all()   
    # Se los enviamos al HTML
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})