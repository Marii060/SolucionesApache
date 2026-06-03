from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .models import Cliente, Moto
from .forms import ClienteForm
from operaciones.models import Credito, CreditoPagado

@login_required
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_motos = Moto.objects.count() 
    
    # Calculamos desde la app operaciones
    suma_creditos = Credito.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    suma_pagos = CreditoPagado.objects.aggregate(total=Sum('monto_pago'))['total'] or 0
    total_cartera = suma_creditos - suma_pagos
    
    contexto = {
        'total_clientes': total_clientes,
        'total_motos': total_motos,
        'total_cartera': total_cartera,
        'total_recaudado': suma_pagos,
    }
    return render(request, 'gestion/dashboard.html', contexto)

#Lista de clientes
@login_required
def lista_clientes(request):
    #Traemos todos los clientes y les "anexamos" el conteo de sus motos
    clientes = Cliente.objects.annotate(cantidad_motos=Count('moto'))
    #Atrapamos lo que el usuario escribió o seleccionó en la fachada (HTML)
    buscar = request.GET.get('buscar', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    #BUSCADOR: Si escribió algo, filtramos por nombre O por documento (icontains ignora mayúsculas)
    if buscar:
        clientes = clientes.filter(
            Q(nombre__icontains=buscar) | 
            Q(numero_documento__icontains=buscar)
        )

    #FILTROS DESPLEGABLES: Si seleccionó un tipo o estado, filtramos por eso
    if tipo:
        clientes = clientes.filter(razon_social=tipo)
        
    if estado:
        clientes = clientes.filter(estado=estado)

    # Enviamos los clientes ya filtrados y listos al HTML
    contexto = {
        'clientes': clientes,
    }
    return render(request, 'gestion/lista_clientes.html', contexto)

#Crear cliente
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, '¡Cliente guardado exitosamente en Soluciones Apache!')
            return redirect('gestion:lista_clientes') 
    else:
        form = ClienteForm()
        
    return render(request, 'gestion/crear_cliente.html', {'form': form})