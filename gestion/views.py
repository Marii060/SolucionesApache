from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
import json
import datetime
from django.core.paginator import Paginator
from django import forms
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from django.core import serializers
from gestion.models import Cliente, Moto, Log, ConfiguracionSistema
from inventario.models import MarcaProducto, Categoria, Proveedor, Producto, MovimientoInventario, Compra, DetalleCompra
from operaciones.models import ListaServicio, Servicio, DetalleServicio, Venta, DetalleVenta, Credito, CreditoPagado
from .forms import ClienteForm, MotoForm, ConfiguracionSistemaForm
from operaciones.models import Credito, CreditoPagado

def personal_required(user):
    return user.is_staff

#Aplicación en la vista del dashboard
@login_required
@user_passes_test(personal_required, login_url='login') # login_url evita errores si no tiene permiso
def dashboard(request):
    # Aquí va toda la lógica de tu dashboard (consultas a la BD, render, etc.)
    return render(request, 'gestion/dashboard.html', {})

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

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.annotate(cantidad_motos=Count('moto')).order_by('-id_cliente')
    buscar = request.GET.get('buscar', '')
    tipo = request.GET.get('tipo', '')
    estado = request.GET.get('estado', '')
    
    if buscar:
        clientes = clientes.filter(
            Q(nombre__icontains=buscar) | 
            Q(numero_documento__icontains=buscar)
        )
    if tipo:
        # Esto filtrará los clientes donde el campo razon_social coincida con el valor enviado
        clientes = clientes.filter(razon_social=tipo)
 
    paginator = Paginator(clientes, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'gestion/lista_cliente.html', {
        'page_obj': page_obj,
        'buscar': buscar, # Útil para mantener la búsqueda al cambiar de página
        'tipo': tipo,
        'estado': estado
    })

# Crear cliente
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente registrado correctamente!')
            return redirect('gestion:lista_cliente')
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
        # Instanciamos el formulario con los datos enviados y la instancia del cliente a editar
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente actualizado correctamente!')
            return redirect('gestion:lista_cliente')
    else:
        # Cargamos el formulario con los datos actuales del cliente para que aparezcan en el HTML
        form = ClienteForm(instance=cliente)
    
    # Renderizamos con el nombre de archivo correcto y la variable 'editando' en True
    return render(request, 'gestion/crear_cliente.html', {
        'form': form, 
        'editando': True 
    })

@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, '¡Cliente eliminado correctamente!')
        return redirect('gestion:lista_cliente')
    return render(request, 'gestion/eliminar.html', {'cliente': cliente})

@login_required
def registrar_moto(request, id_cliente=None):
    # Si viene un id_cliente, buscamos al cliente para pre-seleccionarlo
    cliente_inicial = None
    if id_cliente:
        cliente_inicial = get_object_or_404(Cliente, pk=id_cliente)

    if request.method == 'POST':
        form = MotoForm(request.POST)
        if form.is_valid():
            #Detenemos el guardado directo en la BD
            moto = form.save(commit=False)
            
            # Si venimos desde el perfil de un cliente, le inyectamos el dueño manualmente
            if cliente_inicial:
                moto.id_cliente = cliente_inicial
                
            # Ahora sí guardamos de forma segura en la base de datos
            moto.save()
            
            messages.success(request, '¡Motocicleta registrada con éxito!')
            
            # Si venía de un perfil de cliente, volvemos allí; si no, a la lista general
            if id_cliente:
                return redirect('gestion:detalle_cliente', cliente_id=id_cliente)
            return redirect('gestion:lista_motos')
    else:
        # Pre-llenamos el formulario si tenemos el cliente
        initial_data = {'id_cliente': cliente_inicial} if cliente_inicial else None
        form = MotoForm(initial=initial_data)

    for field in form.fields.values():
        if isinstance(field.widget, forms.Select):
            field.widget.attrs.update({'class': 'form-select'})
        else:
            field.widget.attrs.update({'class': 'form-control'})
    
    return render(request, 'gestion/registrar_moto.html', {
        'form': form, 
        'cliente': cliente_inicial
    })
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
    paginator = Paginator(motos_list, 7) 
    page_number = request.GET.get('page')
    motos = paginator.get_page(page_number)
    
    return render(request, 'gestion/lista_motos.html', {'motos': motos})

# Detalle moto
def detalle_moto(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    return render(request, 'gestion/detalle_moto.html', {'moto': moto})

# Editar moto
def editar_moto(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        form = MotoForm(request.POST, instance=moto)
        if form.is_valid():
            form.save()
            return redirect('gestion:lista_motos')
    else:
        form = MotoForm(instance=moto)
        # Aplicamos estilos a los campos del formulario
        for field in form.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
                
    return render(request, 'gestion/registrar_moto.html', {'form': form, 'moto': moto})

# Eliminar moto
def eliminar_moto(request, pk):
    moto = get_object_or_404(Moto, pk=pk)
    if request.method == 'POST':
        moto.delete()
        return redirect('gestion:lista_motos')
    return render(request, 'gestion/eliminar_moto.html', {'moto': moto})

@login_required
def panel_configuracion(request):
    config = ConfiguracionSistema.obtener_config()
    
    if request.method == 'POST':
        form = ConfiguracionSistemaForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Configuración de Soluciones Apache actualizada correctamente!')
            return redirect('panel_configuracion') # Ajusta esto al nombre de tu URL
    else:
        form = ConfiguracionSistemaForm(instance=config)
    
    return render(request, 'gestion/panel_configuracion.html', {
        'config': config,
        'form': form,
    })

@login_required
def crear_backup_manual(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar copias de seguridad.')
        return redirect('panel_configuracion')

    modelos_a_respaldar = [
        ConfiguracionSistema,
        Cliente,
        MarcaProducto,
        Categoria,
        Proveedor,
        ListaServicio,
        Moto,          
        Producto,      
        Compra,       
        Venta,        
        Servicio,      
        MovimientoInventario,
        DetalleCompra,    
        DetalleVenta,    
        DetalleServicio,  
        Credito,          
        CreditoPagado,    
        Log,              
        ]
    
    data_consolidada = []
    for modelo in modelos_a_respaldar:
        queryset = modelo.objects.all()
        serialized_data = serializers.serialize('json', queryset, indent=2)
        model_data_list = json.loads(serialized_data)
        data_consolidada.extend(model_data_list)

    final_json_data = json.dumps(data_consolidada, indent=2)

    fecha_hoy = datetime.date.today().strftime("%Y-%m-%d")
    nombre_archivo = f"backup_soluciones_apache_{fecha_hoy}.json"
    
    response = HttpResponse(final_json_data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    
    config = ConfiguracionSistema.obtener_config()
    config.ultima_copia_seguridad = datetime.datetime.now()
    config.save()
    
    messages.success(request, '¡Backup generado exitosamente!')
    return response