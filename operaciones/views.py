from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utils import render_to_pdf
from decimal import Decimal
import calendar
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.core.paginator import Paginator
from operaciones.models import Servicio, DetalleServicio, ListaServicio, Venta, DetalleVenta, Credito, CreditoPagado
from gestion.models import Cliente, Moto, ConfiguracionSistema
from inventario.models import Producto, Compra
from .forms import ServicioForm, ListaServicioForm, VentaForm, AbonoForm

@login_required
def lista_catalogo(request):
    query = request.GET.get('buscar', '')
    if query:
        lista_servicios = ListaServicio.objects.filter(nombre_servicio__icontains=query).order_by('id_lista_servicio')
    else:
        lista_servicios = ListaServicio.objects.all().order_by('id_lista_servicio')
    
    paginator = Paginator(lista_servicios, 10)
    page_number = request.GET.get('page')
    servicios = paginator.get_page(page_number)
    
    return render(request, 'operaciones/lista_catalogo.html', {'servicios': servicios, 'query': query})

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
    servicio = get_object_or_404(ListaServicio, id_lista_servicio=id)
    if request.method == 'POST':
        form = ListaServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Servicio actualizado correctamente!')
            return redirect('operaciones:lista_catalogo')
    else:
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
    query = request.GET.get('buscar', '')
    estado_filtro = request.GET.get('estado', 'Todos')
    lista_ordenes = Servicio.objects.all()

    if query:
        lista_ordenes = lista_ordenes.filter(
            Q(codigo_servicio__icontains=query) | 
            Q(id_moto__placa__icontains=query)
        )

    if estado_filtro != 'Todos':
        lista_ordenes = lista_ordenes.filter(estado=estado_filtro)

    lista_ordenes = lista_ordenes.order_by('-id_servicio')
    paginator = Paginator(lista_ordenes, 10)
    page_number = request.GET.get('page')
    ordenes = paginator.get_page(page_number)
    
    config = ConfiguracionSistema.obtener_config()
    
    return render(request, 'operaciones/lista_servicios.html', {
        'ordenes': ordenes, 'query': query, 'estado_actual': estado_filtro, 'config': config
    })
    
@login_required
@transaction.atomic # Protege el proceso de inventario y creación
def crear_servicio(request):
    clientes = Cliente.objects.all()
    motos = Moto.objects.none() 
    servicios_taller = ListaServicio.objects.filter(estado=True)
    productos_inventario = Producto.objects.filter(disponible=True, cantidad__gt=0)

    if request.method == 'POST':
        data = request.POST.copy()
        if 'moto' in data and data['moto']:
            data['id_moto'] = data['moto']
        data['estado'] = 'Pendiente'
        
        if not data.get('codigo_servicio'):
            ultimo_servicio = Servicio.objects.order_by('-id_servicio').first()
            siguiente_num = (ultimo_servicio.id_servicio + 1) if ultimo_servicio else 1000
            data['codigo_servicio'] = f"OS-{siguiente_num}"
            
        form = ServicioForm(data)
        
        if form.is_valid():
            servicio = form.save(commit=False) 
            servicio.id_usuario = request.user 
            mano_obra = float(request.POST.get('valor_mano_obra') or 0)
            total_productos = float(request.POST.get('total_productos_oculto') or 0)
            servicio.valor_mano_obra = mano_obra
            servicio.valor_total = mano_obra + total_productos
            servicio.save()
            
            servicios_id = request.POST.getlist('servicios_id[]')
            productos_id = request.POST.getlist('productos_id[]')
            productos_cant = request.POST.getlist('productos_cant[]')
            productos_precio = request.POST.getlist('productos_precio[]')

            # 1. Guardar Servicios
            for s_id in servicios_id:
                lista_servicio = ListaServicio.objects.get(id_lista_servicio=s_id)
                DetalleServicio.objects.create(
                    id_servicio=servicio,
                    id_lista_servicio=lista_servicio,
                    precio_unitario=lista_servicio.precio_base_mano_obra,
                    total=lista_servicio.precio_base_mano_obra,
                    tipo='Mano de obra'
                )

            # 2. Guardar Productos y descontar inventario
            if productos_id:
                for p_id, cant, precio in zip(productos_id, productos_cant, productos_precio):
                    cantidad_usada = int(cant)
                    producto = Producto.objects.get(id_producto=p_id)
                    
                    DetalleServicio.objects.create(
                        id_servicio=servicio,
                        id_producto=producto,
                        cantidad=cantidad_usada,
                        precio_unitario=float(precio),
                        total=cantidad_usada * float(precio),
                        tipo='Repuesto'
                    )
                    
                    # Descuento de inventario
                    producto.cantidad -= cantidad_usada
                    if producto.cantidad <= 0:
                        producto.disponible = False
                        producto.cantidad = 0
                    producto.save()
            
            messages.success(request, '¡Orden creada y detalles guardados con éxito!')
            return redirect('operaciones:lista_servicios') 
        else:
            motos = Moto.objects.filter(id_cliente=data.get('cliente'))
    else:
        form = ServicioForm()
        
    return render(request, 'operaciones/registrar_servicio.html', {
        'form': form, 'clientes': clientes, 'motos': motos,
        'servicios_taller': servicios_taller, 'productos': productos_inventario
    })

@login_required
def obtener_motos_cliente(request, cliente_id):
    motos = Moto.objects.filter(id_cliente=cliente_id)
    motos_data = [{'id': m.id_moto, 'texto': f"{m.marca} {m.modelo} — Placa: {m.placa}"} for m in motos]
    return JsonResponse(motos_data, safe=False)

@login_required
def detalle_servicio(request, id):
    orden = get_object_or_404(Servicio, id_servicio=id)
    return render(request, 'operaciones/detalle_servicio.html', {'orden': orden})

@login_required
def actualizar_estado(request, id):
    if request.method == 'POST':
        orden = get_object_or_404(Servicio, id_servicio=id)
        orden.estado = request.POST.get('estado')
        orden.save()
    return redirect('operaciones:lista_servicios')

@login_required
def asignar_mecanico(request, id):
    if request.method == 'POST':
        orden = get_object_or_404(Servicio, id_servicio=id)
        orden.mecanico = request.POST.get('mecanico_nombre')
        orden.save()
    return redirect('operaciones:lista_servicios')

@login_required
def generar_recibo(request, servicio_id):
    orden = get_object_or_404(Servicio, pk=servicio_id)
    detalles = DetalleServicio.objects.filter(id_servicio=orden)
    return render(request, 'operaciones/generar_recibo.html', {'orden': orden, 'detalles': detalles})

@login_required
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')
    buscar = request.GET.get('buscar')
    if buscar:
        ventas = ventas.filter(
            Q(num_factura__icontains=buscar) | Q(id_cliente__nombre__icontains=buscar) | 
            Q(id_cliente__numero_documento__icontains=buscar) 
        )
    tipo_pago = request.GET.get('tipo_pago')
    if tipo_pago:
        ventas = ventas.filter(tipo_pago=tipo_pago)
    
    # Manejo de fechas
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
            'form': form, 'productos': productos,
            'iva_actual': config.iva_porcentaje, 'tipo_doc': config.tipo_documento
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
                            id_venta=venta, id_producto=producto,
                            cantidad=item['cantidad'], precio_unitario=item['precio'],
                            total=item['subtotal'], tipo='Producto'
                        )
                        producto.cantidad -= int(item['cantidad'])
                        producto.save()

                    if venta.tipo_pago == 'Credito':
                        Credito.objects.create(
                            cliente=venta.id_cliente, venta=venta,
                            valor_total=venta.total_venta, saldo_pendiente=venta.total_venta,
                            estado='ACTIVO'
                        )

                    messages.success(request, f'¡Venta #{venta.num_factura} registrada con éxito!')
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
    if venta.estado:
        venta.estado = False
        venta.save()
        messages.warning(request, f'Venta #{venta.num_factura} anulada correctamente.')
    return redirect('operaciones:lista_ventas')

@login_required
def imprimir_recibo(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'operaciones/imprimir_recibo.html', {'venta': venta})

@login_required
def lista_creditos(request):
    query = request.GET.get('buscar', '')
    estado_filtro = request.GET.get('estado', 'Todos')
    creditos = Credito.objects.all().order_by('-fecha_creacion')

    if query:
        creditos = creditos.filter(Q(cliente__nombre__icontains=query) | Q(venta__num_factura__icontains=query))
    if estado_filtro != 'Todos':
        creditos = creditos.filter(estado=estado_filtro)

    # Fecha actual para comparar vencimientos
    today = timezone.now().date() 

    for c in creditos:
        # 1. Cálculo de porcentaje
        if c.valor_total and c.valor_total > 0:
            pagado = c.valor_total - c.saldo_pendiente
            c.porcentaje = int((pagado / c.valor_total) * 100)
        else:
            c.porcentaje = 0
        if c.estado == 'PAGADO':
            c.status_label = "Pagado"
            c.badge_color = "bg-success"
        elif hasattr(c, 'fecha_vencimiento') and c.fecha_vencimiento and c.fecha_vencimiento < today:
            c.status_label = "Vencido"
            c.badge_color = "bg-danger" 
        else:
            c.status_label = "Vigente"
            c.badge_color = "bg-warning text-dark"

    paginator = Paginator(creditos, 10)
    page_number = request.GET.get('page')
    creditos_page = paginator.get_page(page_number)

    return render(request, 'operaciones/lista_creditos.html', {
        'creditos': creditos_page,
        'query': query,
        'estado_actual': estado_filtro
    })

@login_required
def obtener_creditos_cliente(request, cliente_id):
    # Traemos solo los créditos activos de ese cliente
    creditos = Credito.objects.filter(cliente_id=cliente_id, estado='ACTIVO')
    creditos_data = [
        {
            'id': c.id, 
            'texto': f"Factura: {c.venta.num_factura if c.venta else 'N/A'} - Saldo: ${c.saldo_pendiente:,.0f}"
        } 
        for c in creditos
    ]
    return JsonResponse(creditos_data, safe=False)

@login_required
def registrar_abono(request):
    # Intentamos obtener el crédito si viene desde la URL
    credito_id = request.GET.get('credito_id')
    credito_pre = None
    if credito_id:
        credito_pre = get_object_or_404(Credito, pk=credito_id)

    if request.method == 'POST':
        form = AbonoForm(request.POST)
        # El credito_id aquí viene del formulario
        c_id = request.POST.get('credito_id') 
        
        if form.is_valid() and c_id:
            with transaction.atomic():
                abono = form.save(commit=False)
                abono.credito = get_object_or_404(Credito, pk=c_id)
                abono.usuario = request.user
                abono.save()
                messages.success(request, "Abono registrado correctamente.")
                return redirect('operaciones:lista_creditos')

    form = AbonoForm()
    clientes = Cliente.objects.all()
    return render(request, 'operaciones/registrar_abono.html', {
        'form': form, 
        'clientes': clientes,
        'credito_pre': credito_pre 
    })

@login_required
def detalle_credito(request, credito_id):
    credito = get_object_or_404(Credito, pk=credito_id)
    # Obtenemos los abonos usando el related_name='abonos'
    abonos = credito.abonos.all().order_by('-fecha_pago')
    return render(request, 'operaciones/detalle_credito.html', {
        'credito': credito,
        'abonos': abonos
    })
 
def obtener_creditos_cliente(request, cliente_id):
    creditos = Credito.objects.filter(cliente_id=cliente_id, estado='ACTIVO')
    creditos_data = [
        {
            'id': c.id, 
            'saldo': float(c.saldo_pendiente), 
            'texto': f"Factura: {c.venta.num_factura if c.venta else 'N/A'} - Saldo: ${c.saldo_pendiente:,.0f}"
        } 
        for c in creditos
    ]
    return JsonResponse(creditos_data, safe=False) 

@login_required
def reportes_estadisticas(request):
    mes_seleccionado = request.GET.get('mes', timezone.now().strftime('%Y-%m'))
    fecha = datetime.strptime(mes_seleccionado, '%Y-%m')
    
    # Cálculos Globales
    ultimo_dia = calendar.monthrange(fecha.year, fecha.month)[1]
    fin_mes = datetime(fecha.year, fecha.month, ultimo_dia, 23, 59, 59)
    
    # Ingresos Totales
    ingresos_servicios = Servicio.objects.filter(fecha_inicio__year=fecha.year, fecha_inicio__month=fecha.month).aggregate(total=Sum('valor_total'))['total'] or 0
    detalles_venta = DetalleVenta.objects.filter(id_venta__fecha_venta__year=fecha.year, id_venta__fecha_venta__month=fecha.month)
    ingresos_productos = detalles_venta.aggregate(total=Sum('total'))['total'] or 0
    
    # Compras y Cartera
    total_compras = Compra.objects.filter(fecha_compra__year=fecha.year, fecha_compra__month=fecha.month).aggregate(total=Sum('total_compra'))['total'] or 0
    cartera_pendiente = Credito.objects.filter(estado='ACTIVO', fecha_creacion__lte=fin_mes).aggregate(total=Sum('saldo_pendiente'))['total'] or 0
    
    #Desglose Semanal (4 Semanas fijas)
    desglose_semanal = []
    rangos = [
        ('Semana 1', 1, 7), 
        ('Semana 2', 8, 14), 
        ('Semana 3', 15, 21), 
        ('Semana 4', 22, ultimo_dia)
    ]
    
    for label, inicio, fin in rangos:
        # Filtros por semana
        ventas_sem = Venta.objects.filter(fecha_venta__year=fecha.year, fecha_venta__month=fecha.month, fecha_venta__day__range=(inicio, fin))
        abonos_sem = CreditoPagado.objects.filter(fecha_pago__year=fecha.year, fecha_pago__month=fecha.month, fecha_pago__day__range=(inicio, fin))
        
        # Cálculos de ingresos
        efectivo = ventas_sem.filter(tipo_pago__icontains='Efectivo').aggregate(total=Sum('total_venta'))['total'] or 0
        creditos = ventas_sem.filter(tipo_pago__icontains='Credito').aggregate(total=Sum('total_venta'))['total'] or 0
        abonos = abonos_sem.aggregate(total=Sum('monto_pago'))['total'] or 0
        
        desglose_semanal.append({
            'semana': label,
            'fechas': f"{inicio:02d} - {fin:02d}",
            'efectivo': efectivo,
            'creditos': creditos,
            'abonos': abonos,
            'total': efectivo + creditos + abonos,
            'qty': ventas_sem.count()
        })
        
    # Top 5 Productos
    top_productos = detalles_venta.values('id_producto__nombre').annotate(
        total_qty=Sum('cantidad'),
        total_sales=Sum('total')
    ).order_by('-total_qty')[:5]

    contexto = {
        'mes_seleccionado': mes_seleccionado,
        'ingresos_servicios': ingresos_servicios,
        'ingresos_productos': ingresos_productos,
        'total_compras': total_compras,
        'cartera_pendiente': cartera_pendiente,
        'flujo_efectivo': (ingresos_servicios + ingresos_productos) - total_compras,
        'top_productos': top_productos,
        'desglose_semanal': desglose_semanal
    }
    if 'exportar' in request.GET:
        pdf = render_to_pdf('operaciones/reporte_pdf.html', contexto)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Reporte_{mes_seleccionado}.pdf"'
            return response

    return render(request, 'operaciones/reportes.html', contexto)