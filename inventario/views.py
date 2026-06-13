from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Categoria
from .forms import CategoriaForm

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