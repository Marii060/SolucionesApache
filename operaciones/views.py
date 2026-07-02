from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from operaciones.models import Servicio, DetalleServicio, ListaServicio, Venta, DetalleVenta, Credito
from gestion.models import Cliente, Moto, ConfiguracionSistema
from inventario.models import Producto
from .forms import ServicioForm, ListaServicioForm, VentaForm

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
    # Capturamos el texto del buscador y el estado seleccionado (por defecto 'Todos')
    query = request.GET.get('buscar', '')
    estado_filtro = request.GET.get('estado', 'Todos')
    lista_ordenes = Servicio.objects.all()

    # Aplicamos filtro de búsqueda si el usuario escribió algo (Código o Placa)
    if query:
        lista_ordenes = lista_ordenes.filter(
            Q(codigo_servicio__icontains=query) | 
            Q(id_moto__placa__icontains=query)
        )

    # Aplicamos filtro por Estado si seleccionó uno diferente a 'Todos'
    if estado_filtro != 'Todos':
        lista_ordenes = lista_ordenes.filter(estado=estado_filtro)

    # Ordenamos para que las más recientes aparezcan arriba
    lista_ordenes = lista_ordenes.order_by('-id_servicio')
    paginator = Paginator(lista_ordenes, 10)
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    
    #configuración global de Soluciones Apache
    config = ConfiguracionSistema.obtener_config()
    
    # Enviamos los datos, los estados actuales y la CONFIGURACIÓN al HTML
    return render(request, 'operaciones/lista_servicios.html', {
        'ordenes': ordenes,
        'query': query,
        'estado_actual': estado_filtro,
        'config': config  
    })
    
@login_required
def crear_servicio(request):
    clientes = Cliente.objects.all()
    # Inicialmente vacías, se llenarán mediante AJAX cuando seleccionen el cliente
    motos = Moto.objects.none() 
    
    # TRAEMOS LOS DATOS REALES DE LA BASE DE DATOS
    servicios_taller = ListaServicio.objects.filter(estado=True) # Solo servicios activos
    productos_inventario = Producto.objects.filter(disponible=True, cantidad__gt=0) # Solo productos con cantidad mayor a 0

    if request.method == 'POST':
        data = request.POST.copy()
        
        # Adaptamos el campo de la moto
        if 'moto' in data and data['moto']:
            data['id_moto'] = data['moto']
            
        # INYECTAMOS LOS DATOS FALTANTES AUTOMÁTICAMENTE
        data['estado'] = 'Pendiente'
        
        if not data.get('codigo_servicio'):
            ultimo_servicio = Servicio.objects.order_by('-id_servicio').first()
            siguiente_num = (ultimo_servicio.id_servicio + 1) if ultimo_servicio else 1000
            data['codigo_servicio'] = f"OS-{siguiente_num}"
            
        form = ServicioForm(data)
        
        if form.is_valid():
            # Guardamos el formulario, el campo 'mecanico' se guarda automáticamente
            servicio = form.save(commit=False) 
            servicio.id_usuario = request.user 
            
            mano_obra_raw = request.POST.get('valor_mano_obra') or 0
            total_prod_raw = request.POST.get('total_productos_oculto') or 0
            
            mano_obra = float(mano_obra_raw)
            total_productos = float(total_prod_raw)
            
            servicio.valor_mano_obra = mano_obra
            servicio.valor_total = mano_obra + total_productos
            servicio.save()
            
            #LISTAS DINÁMICAS
            servicios_id = request.POST.getlist('servicios_id[]')
            productos_id = request.POST.getlist('productos_id[]')
            productos_cant = request.POST.getlist('productos_cant[]')

            # Procesamos mano de obra
            for s_id in servicios_id:
                # Aquí iría tu lógica de guardado de la tabla pivote de servicios
                pass

            #Descuento del inventario
            if productos_id:
                for p_id, cant in zip(productos_id, productos_cant):
                    cantidad_usada = int(cant)
                    try:
                        # Buscamos el producto exacto
                        producto = Producto.objects.get(id_producto=p_id)
                        
                        # Le restamos la cantidad a la columna 'cantidad'
                        producto.cantidad -= cantidad_usada
                        
                        # Si la cantidad llega a 0, lo marcamos como no disponible
                        if producto.cantidad <= 0:
                            producto.disponible = False
                            
                        producto.save()
                        
                        # Aquí iría tu lógica de guardado de la tabla pivote de repuestos
                        
                    except Producto.DoesNotExist:
                        pass # Por si envían un ID que no existe
            
            messages.success(request, '¡Orden de servicio creada con éxito y el inventario fue actualizado!')
            return redirect('operaciones:lista_servicios') 
        else:
            print("Errores de validación en la orden:", form.errors)
            # Pasamos las variables nuevamente para que no se pierdan los clientes al recargar
            motos = Moto.objects.filter(id_cliente=data.get('cliente'))
    else:
        form = ServicioForm()
        
    # Agregamos los servicios y productos al diccionario de contexto
    return render(request, 'operaciones/registrar_servicio.html', {
        'form': form,
        'clientes': clientes,
        'motos': motos,
        'servicios_taller': servicios_taller,
        'productos': productos_inventario
    })
    
#Buscador de motos por cliente
@login_required
def obtener_motos_cliente(request, cliente_id):
    # Buscamos todas las motos que pertenezcan a ese cliente específico
    motos = Moto.objects.filter(id_cliente=cliente_id)
    
    # Preparamos los datos en formato JSON para enviarlos a la pantalla
    motos_data = []
    for m in motos:
        motos_data.append({
            'id': m.id_moto,
            'texto': f"{m.marca} {m.modelo} — Placa: {m.placa}"
        })
        
    return JsonResponse(motos_data, safe=False)

@login_required
def detalle_servicio(request, id):
    # Buscamos la orden
    orden = get_object_or_404(Servicio, id_servicio=id)
    
    # Calculamos cuánto se gastó solo en repuestos
    total_repuestos = orden.valor_total - orden.valor_mano_obra
    
    return render(request, 'operaciones/detalle_servicio.html', {
        'orden': orden,
        'total_repuestos': total_repuestos 
    })

@login_required
def actualizar_estado(request, id):
    if request.method == 'POST':
        orden = get_object_or_404(Servicio, id_servicio=id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in ['Pendiente', 'En Proceso', 'Terminado', 'Entregado']:
            orden.estado = nuevo_estado
            orden.save()
            messages.success(request, f'¡Estado de la orden {orden.codigo_servicio} actualizado a {nuevo_estado}!')
            
    return redirect('operaciones:lista_servicios')

@login_required
def asignar_mecanico(request, id):
    if request.method == 'POST':
        orden = get_object_or_404(Servicio, id_servicio=id)
        nombre_mecanico = request.POST.get('mecanico_nombre')
        
        orden.mecanico = nombre_mecanico
        orden.save()
        messages.success(request, f'¡Mecánico "{nombre_mecanico}" asignado con éxito a la orden {orden.codigo_servicio}!')
        
    return redirect('operaciones:lista_servicios')

@login_required
def generar_recibo(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    detalles = DetalleServicio.objects.filter(id_servicio=servicio)
    config = ConfiguracionSistema.obtener_config()
    
    mano_obra = 0
    repuestos = 0
    
    # Intentamos sumar los detalles (si los ingresaste uno por uno)
    for item in detalles:
        valor = float(item.total or (item.precio_unitario * item.cantidad) or 0)
        
        if item.id_producto or (item.tipo and 'repuesto' in str(item.tipo).lower()):
            repuestos += valor
        else:
            mano_obra += valor
    # Si la orden no tiene detalles registrados uno a uno, tomamos los valores
    # directamente de la orden principal de tu modelo Servicio.
    if mano_obra == 0 and repuestos == 0:
        mano_obra = float(servicio.valor_mano_obra or 0)
        total_orden = float(servicio.valor_total or 0)
        
        # Lógica matemática: Si sabemos el total y la mano de obra, el resto son repuestos.
        # Ejemplo de Fredy: 185.000 (Total) - 30.000 (Mano de obra) = 155.000 (Repuestos)
        if total_orden > mano_obra:
            repuestos = total_orden - mano_obra

    # Cálculos de Impuestos
    porcentaje_iva = float(config.iva_porcentaje or 0)
    
    # El IVA se aplica ÚNICAMENTE a la bolsa de repuestos
    monto_iva = repuestos * (porcentaje_iva / 100)
    
    # Totales finales
    subtotal_general = mano_obra + repuestos
    total_general = subtotal_general + monto_iva

    contexto = {
        'servicio': servicio,
        'config': config,
        'mano_obra': mano_obra,
        'repuestos': repuestos,
        'subtotal_general': subtotal_general, 
        'monto_iva': monto_iva,
        'total_general': total_general,
    }
    
    return render(request, 'operaciones/generar_recibo.html', contexto)

@login_required
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')
    buscar = request.GET.get('buscar')
    if buscar:
        ventas = ventas.filter(
            Q(num_factura__icontains=buscar) |
            Q(id_cliente__nombre__icontains=buscar) | 
            Q(id_cliente__numero_documento__icontains=buscar) 
        )

    tipo_pago = request.GET.get('tipo_pago')
    if tipo_pago:
        ventas = ventas.filter(tipo_pago=tipo_pago)

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_venta__lte=fecha_fin + ' 23:59:59')

    paginator = Paginator(ventas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'operaciones/lista_ventas.html', {'ventas': page_obj})

@login_required
def crear_venta(request):
    if request.method == 'GET':
        form = VentaForm()
        productos = Producto.objects.filter(disponible=True)
        config = ConfiguracionSistema.obtener_config()
        
        return render(request, 'operaciones/crear_venta.html', {
            'form': form,
            'productos': productos,
            'iva_actual': config.iva_porcentaje,
            'tipo_doc': config.tipo_documento
        })
        
    elif request.method == 'POST':
        form = VentaForm(request.POST)
        productos_json = request.POST.get('productos_json')
        subtotal_recibido = Decimal(request.POST.get('total_venta', 0))

        if form.is_valid() and productos_json:
            try:
                with transaction.atomic():
                    config = ConfiguracionSistema.obtener_config()
                    
                    monto_iva = Decimal('0.00')
                    total_final = subtotal_recibido
                    tipo_doc_venta = 'RECIBO'
                    
                    if config.maneja_iva:
                        iva_factor = config.iva_porcentaje / Decimal('100')
                        monto_iva = (subtotal_recibido * iva_factor).quantize(Decimal('1.00'))
                        total_final = subtotal_recibido + monto_iva
                        tipo_doc_venta = 'FACTURA'

                    venta = form.save(commit=False)
                    ultima_venta = Venta.objects.order_by('-num_factura').first()
                    venta.num_factura = (ultima_venta.num_factura + 1) if ultima_venta else 1
                    
                    venta.fecha_venta = timezone.now()
                    venta.total_venta = total_final 
                    venta.monto_iva = monto_iva     
                    venta.tipo_documento = tipo_doc_venta 
                    venta.id_usuario = request.user
                    venta.save()

                    productos_data = json.loads(productos_json)
                    for item in productos_data:
                        producto = Producto.objects.get(id_producto=item['id'])
                        DetalleVenta.objects.create(
                            id_venta=venta,
                            id_producto=producto,
                            cantidad=item['cantidad'],
                            precio_unitario=item['precio'],
                            total=item['subtotal'],
                            tipo='Producto'
                        )
                        producto.cantidad -= int(item['cantidad'])
                        producto.save()

                    if venta.tipo_pago == 'Credito':
                        Credito.objects.create(
                            cliente=venta.id_cliente,
                            venta=venta,
                            valor_total=venta.total_venta, 
                            saldo_pendiente=venta.total_venta,
                            estado='ACTIVO'
                        )

                    messages.success(request, f'¡Venta #{venta.num_factura} ({tipo_doc_venta}) registrada con éxito!')
                    return redirect('operaciones:lista_ventas')
                    
            except Exception as e:
                messages.error(request, f'Error al registrar la venta: {str(e)}')
                return redirect('operaciones:crear_venta')
        else:
            messages.error(request, 'Datos inválidos.')
            return redirect('operaciones:crear_venta')

@login_required
def detalle_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'operaciones/detalle_venta.html', {'venta': venta})

@login_required
def anular_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    
    # Solo anulamos si no está anulada ya
    if venta.estado:
        venta.estado = False # Marcamos como anulada (o inactiva)
        venta.save()
        messages.warning(request, f'Venta #{venta.num_factura} anulada correctamente.')
    
    return redirect('operaciones:lista_ventas')

@login_required
def imprimir_recibo(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    # Por ahora, simplemente renderizamos una página que el navegador pueda imprimir
    # Luego crearemos el PDF cuando necesites un archivo descargable
    return render(request, 'operaciones/imprimir_recibo.html', {'venta': venta})



 