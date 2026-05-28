from django.db import models
from django.contrib.auth.models import User
from gestion.models import Cliente, Moto 
from inventario.models import Producto

# Es el menú de trabajos que ofrece el taller.
class ListaServicio(models.Model):
    id_lista_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=150)
    precio_base_mano_obra = models.DecimalField(max_digits=12, decimal_places=2)
    estado = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Catálogo de Servicio"
        verbose_name_plural = "Catálogo de Servicios"

    def __str__(self):
        return self.nombre_servicio

# El registro general cuando entra una moto a reparación.
class Servicio(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Terminado', 'Terminado'),
        ('Entregado', 'Entregado'),
    ]

    id_servicio = models.AutoField(primary_key=True)
    codigo_servicio = models.CharField(max_length=20, unique=True)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    valor_mano_obra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    descripcion = models.TextField(blank=True, null=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    id_moto = models.ForeignKey(Moto, on_delete=models.CASCADE, db_column='id_moto')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        verbose_name = "Orden de Servicio"
        verbose_name_plural = "Órdenes de Servicio"

    def __str__(self):
        return f"Servicio {self.codigo_servicio} - {self.id_moto.placa}"

# Aquí anotamos cada repuesto y trabajo gastado en la moto.
class DetalleServicio(models.Model):
    id_detalle_servicio = models.AutoField(primary_key=True)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='detalles', db_column='id_servicio')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True, db_column='id_producto')
    id_lista_servicio = models.ForeignKey(ListaServicio, on_delete=models.CASCADE, db_column='id_lista_servicio')
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tipo = models.CharField(max_length=50, blank=True, null=True) #'Repuesto' o 'Mano de obra'

    class Meta:
        verbose_name = "Detalle del Servicio"
        verbose_name_plural = "Detalles de los Servicios"
        

# Cuando vendemos un repuesto a un cliente que no metió la moto al taller.
class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    num_factura = models.IntegerField(unique=True)
    fecha_venta = models.DateTimeField()
    tipo_pago = models.CharField(max_length=90)
    total = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.BooleanField(default=True)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def __str__(self):
        return f"Factura {self.num_factura}"

# La lista de productos que el cliente se llevó en la factura.
class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=0)
    total = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    tipo = models.CharField(max_length=90)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles_venta', db_column='id_venta')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"

# Para llevar la cuenta de los clientes que fiaron (en taller o en mostrador).
class CreditoPagado(models.Model):
    id_credito = models.AutoField(primary_key=True)
    monto_pago = models.DecimalField(max_digits=10, decimal_places=0)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    metodo_pago = models.CharField(max_length=50)
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_usuario')
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE, db_column='id_venta', null=True, blank=True)
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, db_column='id_servicio', null=True, blank=True)

    class Meta:
        verbose_name = "Abono de Crédito"
        verbose_name_plural = "Abonos de Créditos"        