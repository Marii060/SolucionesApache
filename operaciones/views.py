from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False) 
            
            # Asignamos automáticamente el usuario de la sesión activa
            servicio.id_usuario = request.user 
            
            # Guardamos definitivamente en MySQL
            servicio.save() 
            
            messages.success(request, '¡Orden de servicio creada con éxito!')
            
            # NOTA: Cambiado temporalmente a lista_catalogo para evitar errores si no has creado la lista de órdenes
            return redirect('operaciones:lista_catalogo') 
    else:
        form = ServicioForm()
        
    return render(request, 'operaciones/registrar_servicio.html', {'form': form})