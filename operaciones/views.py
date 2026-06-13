from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Servicio, ListaServicio
from .forms import ServicioForm, ListaServicioForm

@login_required
def lista_catalogo(request):
    # Capturamos lo que el usuario escribió en el buscador
    query = request.GET.get('buscar', '')

    # Filtramos por coincidencia si hay texto en la barra
    if query:
        lista_servicios = ListaServicio.objects.filter(nombre_servicio__icontains=query).order_by('id_lista_servicio')
    else:
        lista_servicios = ListaServicio.objects.all().order_by('id_lista_servicio')
    
    # Paginación de a 10 registros
    paginator = Paginator(lista_servicios, 10)
    page_number = request.GET.get('page')
    servicios = paginator.get_page(page_number)
    
    return render(request, 'operaciones/lista_catalogo.html', {
        'servicios': servicios,
        'query': query 
    })

@login_required
def crear_catalogo(request):
    if request.method == 'POST':
        form = ListaServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Servicio agregado al catálogo exitosamente!')
            return redirect('operaciones:lista_catalogo')
    else:
        form = ListaServicioForm()
        
    return render(request, 'operaciones/registrar_catalogo.html', {'form': form})

@login_required
def editar_catalogo(request, id):
    # Buscamos el servicio específico usando su ID
    servicio = get_object_or_404(ListaServicio, id_lista_servicio=id)
    
    if request.method == 'POST':
        # Le pasamos el 'instance=servicio' para que sobreescriba, no cree uno nuevo
        form = ListaServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Servicio actualizado correctamente!')
            return redirect('operaciones:lista_catalogo')
    else:
        # Cargamos el formulario con los datos que ya tiene el servicio
        form = ListaServicioForm(instance=servicio)
        
    return render(request, 'operaciones/registrar_catalogo.html', {'form': form, 'servicio': servicio})

@login_required
def eliminar_catalogo(request, id):
    servicio = get_object_or_404(ListaServicio, id_lista_servicio=id)
    
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, '¡Servicio eliminado del catálogo exitosamente!')
        return redirect('operaciones:lista_catalogo')
        
    return render(request, 'operaciones/eliminar_catalogo.html', {'servicio': servicio})

@login_required
def lista_servicios(request):
    #Capturamos el texto del buscador y el estado seleccionado (por defecto 'Todos')
    query = request.GET.get('buscar', '')
    estado_filtro = request.GET.get('estado', 'Todos')
    lista_ordenes = Servicio.objects.all()

    #Aplicamos filtro de búsqueda si el usuario escribió algo (Código o Placa)
    if query:
        lista_ordenes = lista_ordenes.filter(
            Q(codigo_servicio__icontains=query) | 
            Q(id_moto__placa__icontains=query)
        )

    #Aplicamos filtro por Estado si seleccionó uno diferente a 'Todos'
    if estado_filtro != 'Todos':
        lista_ordenes = lista_ordenes.filter(estado=estado_filtro)

    #Ordenamos para que las más recientes aparezcan arriba
    lista_ordenes = lista_ordenes.order_by('-id_servicio')
    
    #Paginacion de a 10 registros
    paginator = Paginator(lista_ordenes, 10)
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    
    #Enviamos los datos y los estados actuales para mantener la selección visual activa
    return render(request, 'operaciones/lista_servicios.html', {
        'ordenes': ordenes,
        'query': query,
        'estado_actual': estado_filtro
    })

@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False) 
            servicio.id_usuario = request.user 
            servicio.save() 
            
            messages.success(request, '¡Orden de servicio creada con éxito!')

            return redirect('operaciones:lista_servicios') 
    else:
        form = ServicioForm()
        
    return render(request, 'operaciones/registrar_servicio.html', {'form': form})