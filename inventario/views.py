from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from inventario.models import Categoria, MarcaProducto, Fabricante, Producto, MovimientoInventario, Proveedor, Compra
from .forms import CategoriaForm, MarcaForm, FabricanteForm ,ProductoForm, ProveedorForm, CompraForm, CompraFormSet

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

@login_required
def lista_fabricantes(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'inventario/lista_fabricantes.html', {'fabricantes': fabricantes})

@login_required
def crear_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Fabricante registrado con éxito!')
            return redirect('inventario:lista_fabricantes')
    else:
        form = FabricanteForm()
    return render(request, 'inventario/registrar_fabricante.html', {'form': form, 'titulo': 'Registrar Fabricante'})

@login_required
def editar_fabricante(request, id):
    fabricante = get_object_or_404(Fabricante, id_fabricante=id)
    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=fabricante)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Fabricante actualizado correctamente!')
            return redirect('inventario:lista_fabricantes')
    else:
        form = FabricanteForm(instance=fabricante)
    return render(request, 'inventario/registrar_fabricante.html', {'form': form, 'fabricante': fabricante, 'titulo': 'Editar Fabricante'})

@login_required
def cambiar_estado_fabricante(request, id):
    fabricante = get_object_or_404(Fabricante, id_fabricante=id)
    #Invertimos el estado actual 
    fabricante.estado = not fabricante.estado
    fabricante.save()
    #Creamos un mensaje dinámico 
    accion = "habilitado" if fabricante.estado else "deshabilitado"
    messages.success(request, f'¡El fabricante "{fabricante.nombre}" ha sido {accion} correctamente!')
    
    return redirect('inventario:lista_fabricantes')

@login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.all().order_by('-fecha_creacion')
    return render(request, 'inventario/lista_proveedores.html', {'proveedores': proveedores})

@login_required
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Proveedor registrado con éxito!')
            return redirect('inventario:lista_proveedores') 
    else:
        form = ProveedorForm()
    
    return render(request, 'inventario/registrar_proveedor.html', {'form': form, 'titulo': 'Nuevo Proveedor'})

@login_required
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Proveedor actualizado correctamente!')
            return redirect('inventario:lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'inventario/registrar_proveedor.html', {'form': form, 'titulo': 'Editar Proveedor'})

@login_required
def cambiar_estado_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    
    #Invertimos el estado (Soft Delete)
    proveedor.activo = not proveedor.activo
    proveedor.save()
    
    accion = "activado" if proveedor.activo else "inactivado"
    messages.success(request, f'¡El proveedor "{proveedor.razon_social}" ha sido {accion}!')
    return redirect('inventario:lista_proveedores')

@login_required
def detalle_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=id)
    return render(request, 'inventario/detalle_proveedor.html', {'proveedor': proveedor})


@login_required
def lista_productos(request):
    query = request.GET.get('buscar', '')
    categoria_id = request.GET.get('categoria', '')
    marca_id = request.GET.get('marca', '')
    fabricante_id = request.GET.get('fabricante', '') 
    #Base de la consulta
    lista = Producto.objects.all()
    
    #Filtramos por nombre, código o FABRICANTE si el usuario escribió algo en el cuadro de texto
    if query:
        lista = lista.filter(
            Q(nombre__icontains=query) | 
            Q(codigo_interno__icontains=query) |
            Q(id_fabricante__nombre__icontains=query) 
        )
        
    #Filtramos por Categoría si seleccionó alguna
    if categoria_id:
        lista = lista.filter(id_categoria_id=categoria_id)
        
    #Filtramos por Marca si seleccionó alguna
    if marca_id:
        lista = lista.filter(id_marca_id=marca_id)
        
    #Filtramos por Fabricante si seleccionó alguno en el menú desplegable
    if fabricante_id:
        lista = lista.filter(id_fabricante_id=fabricante_id)
        
    #Ordenamos alfabéticamente por código
    lista = lista.order_by('codigo_interno')
        
    # Paginación
    paginator = Paginator(lista, 10)
    page_number = request.GET.get('page')
    productos = paginator.get_page(page_number)
    
    # Consultamos las tablas para llenar los <select> del HTML
    categorias = Categoria.objects.filter(estado=True)
    marcas = MarcaProducto.objects.all()
    fabricantes = Fabricante.objects.filter(estado=True) #Traemos solo los activos
    
    return render(request, 'inventario/lista_productos.html', {
        'productos': productos,
        'query': query,
        'categoria_sel': categoria_id,
        'marca_sel': marca_id,
        'fabricante_sel': fabricante_id, #mantener el filtro visible
        'categorias': categorias,
        'marcas': marcas,
        'fabricantes': fabricantes   #Para armar el <select> en el HTML
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto registrado en el inventario con éxito!')
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/registrar_producto.html', {'form': form})

@login_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto actualizado correctamente!')
            return redirect('inventario:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/registrar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    
    # Si el usuario confirma la eliminación (llega por método POST)
    if request.method == 'POST':
        nombre_producto = producto.nombre 
        producto.delete()
        messages.success(request, f'¡El producto "{nombre_producto}" ha sido eliminado del inventario!')
        return redirect('inventario:lista_productos')
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})

@login_required
def control_inventario(request):
    # Capturamos filtros
    query = request.GET.get('buscar', '')
    tipo = request.GET.get('tipo', '')
    fecha = request.GET.get('fecha', '')
    
    # Base de datos de movimientos
    lista = MovimientoInventario.objects.all().select_related('producto', 'usuario')
    
    # Aplicamos filtros
    if query:
        lista = lista.filter(
            Q(producto__nombre__icontains=query) | 
            Q(referencia__icontains=query)
        )
    if tipo:
        lista = lista.filter(tipo=tipo)
    if fecha:
        lista = lista.filter(fecha_movimiento__date=fecha)
        
    paginator = Paginator(lista, 10)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    
    return render(request, 'inventario/control_inventario.html', {
        'movimientos': movimientos,
        'query': query,
        'tipo_sel': tipo,
        'fecha_sel': fecha
    })

@login_required
def ajuste_manual(request):
    # Traemos solo productos activos
    productos = Producto.objects.filter(disponible=True).order_by('nombre')
    
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        tipo_ajuste = request.POST.get('tipo_ajuste')
        cantidad = int(request.POST.get('cantidad', 0))
        motivo = request.POST.get('motivo')
        observaciones = request.POST.get('observaciones', '')
        
        producto = get_object_or_404(Producto, id_producto=producto_id)
        stock_anterior = producto.cantidad
        
        # Calcular nuevos valores
        if tipo_ajuste == 'Salida':
            stock_nuevo = stock_anterior - cantidad
            cant_registro = -cantidad # Negativo para la tabla
        else:
            stock_nuevo = stock_anterior + cantidad
            cant_registro = cantidad
            
        # 1. Actualizamos el producto físico
        producto.cantidad = stock_nuevo
        producto.save()
        
        # 2. Grabamos el movimiento en la auditoría
        MovimientoInventario.objects.create(
            producto=producto,
            tipo=tipo_ajuste,
            cantidad=cant_registro,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=motivo,
            referencia=f"ADJ-{producto.codigo_interno}",
            observaciones=observaciones,
            usuario=request.user
        )
        
        messages.success(request, '¡Ajuste de inventario registrado con éxito!')
        return redirect('inventario:control_inventario')
        
    return render(request, 'inventario/ajuste_manual.html', {'productos': productos})

@login_required
def abastecer_stock(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        motivo = "Abastecimiento Rápido desde Catálogo"
        
        # Lógica de actualización (similar al ajuste manual)
        stock_anterior = producto.cantidad
        stock_nuevo = stock_anterior + cantidad
        
        producto.cantidad = stock_nuevo
        producto.save()
        
        MovimientoInventario.objects.create(
            producto=producto,
            tipo='Entrada',
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            motivo=motivo,
            referencia=f"ABS-{producto.codigo_interno}",
            usuario=request.user
        )
        
        messages.success(request, f'¡{cantidad} unidades agregadas a "{producto.nombre}"!')
        return redirect('inventario:lista_productos')
        
    return render(request, 'inventario/abastecer_producto.html', {'producto': producto})

@login_required
def lista_compras(request):
    compras = Compra.objects.all().order_by('-fecha_recepcion')
    return render(request, 'inventario/lista_compras.html', {'compras': compras})

@login_required
def registrar_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        formset = CompraFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            compra = form.save(commit=False)
            compra.id_usuario = request.user 
            compra.save()
            # Guardamos los detalles y actualizamos inventario
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.id_compra = compra
                detalle.save()
                # ACTUALIZACIÓN AUTOMÁTICA DE STOCK
                producto = detalle.id_producto
                producto.cantidad += detalle.cantidad
                producto.save()
                
            messages.success(request, f'Compra {compra.codigo_interno} registrada y stock actualizado.')
            return redirect('inventario:lista_compras')
    else:
        form = CompraForm()
        formset = CompraFormSet()
        
    return render(request, 'inventario/registrar_compra.html', {'form': form, 'formset': formset})

@login_required
def detalle_compra(request, id):
    compra = get_object_or_404(Compra, id_compra=id)
    detalles = compra.detalles.all() 
    
    return render(request, 'inventario/detalle_compra.html', {
        'compra': compra,
        'detalles': detalles
    })

@login_required
def actualizar_estado_compra(request, id):
    if request.method == 'POST':
        compra = get_object_or_404(Compra, id_compra=id)
        nuevo_estado = request.POST.get('estado')
        nuevo_estado_pago = request.POST.get('estado_pago')
        if nuevo_estado:
            compra.estado = nuevo_estado
        if nuevo_estado_pago:
            compra.estado_pago = nuevo_estado_pago
            
        compra.save()
        messages.success(request, "Estados actualizados correctamente.")
        
    return redirect('inventario:detalle_compra', id=id)
@login_required
def cancelar_compra(request, id):
    compra = get_object_or_404(Compra, id_compra=id)
    # Hacemos el "Soft Delete" contable: Cambiar a Cancelado
    if compra.estado != 'Cancelado':
        compra.estado = 'Cancelado'
        compra.save()
        messages.success(request, f'La compra {compra.codigo_interno} ha sido anulada (Cancelada).')
    else:
        messages.warning(request, 'Esta compra ya se encontraba cancelada.')
        
    return redirect('inventario:lista_compras')