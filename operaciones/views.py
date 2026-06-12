from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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