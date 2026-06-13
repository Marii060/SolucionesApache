from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Categoria, MarcaProducto
from .forms import CategoriaForm, MarcaForm

@login_required
def lista_categorias(request):
    query = request.GET.get('buscar', '')
    
    if query:
        lista = Categoria.objects.filter(nombre__icontains=query).order_by('codigo_interno')
    else:
        lista = Categoria.objects.all().order_by('codigo_interno')
        
    paginator = Paginator(lista, 10)
    page_number = request.GET.get('page')
    categorias = paginator.get_page(page_number)
    
    return render(request, 'inventario/lista_categorias.html', {
        'categorias': categorias,
        'query': query
    })

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría registrada con éxito!')
            return redirect('inventario:lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'inventario/registrar_categoria.html', {'form': form})

@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id_categoria=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Categoría actualizada correctamente!')
            return redirect('inventario:lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'inventario/registrar_categoria.html', {'form': form, 'categoria': categoria})

@login_required
def inactivar_categoria(request, id):
    # Buscamos la categoría por su ID
    categoria = get_object_or_404(Categoria, id_categoria=id)
    # Cambiamos su estado a False (Inactivo)
    categoria.estado = False
    categoria.save()
    messages.success(request, f'¡La categoría "{categoria.nombre}" ha sido inactivada correctamente!')
    return redirect('inventario:lista_categorias')

# Vistas para MarcaProducto
@login_required
def lista_marcas(request):
    query = request.GET.get('buscar', '')
    
    if query:
        lista = MarcaProducto.objects.filter(nombre__icontains=query).order_by('id_marca')
    else:
        lista = MarcaProducto.objects.all().order_by('id_marca')
        
    paginator = Paginator(lista, 10)
    page_number = request.GET.get('page')
    marcas = paginator.get_page(page_number)
    
    return render(request, 'inventario/lista_marcas.html', {
        'marcas': marcas,
        'query': query
    })

@login_required
def crear_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Marca registrada con éxito!')
            return redirect('inventario:lista_marcas')
    else:
        form = MarcaForm()
    return render(request, 'inventario/registrar_marca.html', {'form': form})

@login_required
def editar_marca(request, id):
    marca = get_object_or_404(MarcaProducto, id_marca=id)
    if request.method == 'POST':
        form = MarcaForm(request.POST, instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Marca actualizada correctamente!')
            return redirect('inventario:lista_marcas')
    else:
        form = MarcaForm(instance=marca)
    return render(request, 'inventario/registrar_marca.html', {'form': form, 'marca': marca})

@login_required
def eliminar_marca(request, id):
    marca = get_object_or_404(MarcaProducto, id_marca=id)
    
    #Solo elimina si no tiene productos
    if marca.producto_set.exists():
        messages.error(request, f'No puedes eliminar la marca "{marca.nombre}" porque tiene productos asociados en el inventario.')
    else:
        marca.delete()
        messages.success(request, f'¡La marca "{marca.nombre}" ha sido eliminada!')
        
    return redirect('inventario:lista_marcas')