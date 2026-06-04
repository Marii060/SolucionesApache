from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum, Count, Q
from .models import Cliente, Moto
from .forms import ClienteForm, MotoForm
from operaciones.models import Credito, CreditoPagado

@login_required
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_motos = Moto.objects.count() 
    
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

# Lista de clientes (Corregido a plural para ser consistente)
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.annotate(cantidad_motos=Count('moto'))
    buscar = request.GET.get('buscar', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    
    if buscar:
        clientes = clientes.filter(
            Q(nombre__icontains=buscar) | 
            Q(numero_documento__icontains=buscar)
        )
    if tipo:
        clientes = clientes.filter(razon_social=tipo) # Asegúrate que 'razon_social' sea el nombre correcto en tu models.py
    if estado:
        clientes = clientes.filter(estado=estado)

    return render(request, 'gestion/lista_cliente.html', {'clientes': clientes})

# Crear cliente
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente guardado exitosamente!')
            return redirect('gestion:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'gestion/crear_cliente.html', {'form': form})

# Detalle de cliente
@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    motos = Moto.objects.filter(id_cliente=cliente)
    
    contexto = {
        'cliente': cliente,
        'motos': motos,
    }
    return render(request, 'gestion/detalle_cliente.html', contexto)

@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente actualizado correctamente!')
            return redirect('gestion:lista_clientes')
    else:
        # Cargamos el formulario con los datos actuales del cliente
        form = ClienteForm(instance=cliente)
    return render(request, 'gestion/crear_cliente.html', {'form': form, 'editando': True})

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, '¡Cliente eliminado correctamente!')
        return redirect('gestion:lista_clientes')
    return render(request, 'gestion/eliminar.html', {'cliente': cliente})

@login_required
def registrar_moto(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    
    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            moto = form.save(commit=False)
            moto.id_cliente = cliente
            moto.save()
            messages.success(request, '¡La moto se ha registrado correctamente!')
            
            return redirect('gestion:detalle_cliente', cliente_id=id_cliente)
    else:
        form = MotoForm()
        
    return render(request, 'gestion/registrar_moto.html', {'form': form, 'cliente': cliente})

@login_required
def lista_motos(request):
    motos_list = Moto.objects.all().order_by('-id_moto') # Las más recientes primero
    # Lógica de búsqueda
    buscar = request.GET.get('buscar')
    if buscar:
        motos_list = motos_list.filter(
            Q(placa__icontains=buscar) | 
            Q(marca__icontains=buscar) |
            Q(id_cliente__nombre__icontains=buscar)
        )
    # Paginación
    paginator = Paginator(motos_list, 8) 
    page_number = request.GET.get('page')
    motos = paginator.get_page(page_number)
    
    return render(request, 'gestion/lista_motos.html', {'motos': motos})