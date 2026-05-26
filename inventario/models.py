from django.db import models
from django.contrib.auth.models import User

class MarcaProducto(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Marca de Producto"
        verbose_name_plural = "Marcas de Productos"

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=20, unique=True)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=12, decimal_places=2)
    disponible = models.BooleanField(default=True)
    cantidad = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')
    id_marca = models.ForeignKey(MarcaProducto, on_delete=models.CASCADE, db_column='id_marca')
    # Relación Muchos a Muchos con Proveedores
    proveedores = models.ManyToManyField(Proveedor, related_name='productos')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
        ('Credito', 'Crédito'),
    ]
    ESTADO_COMPRA_CHOICES = [
        ('Recibido', 'Recibido'),
        ('Pendiente', 'Pendiente'),
        ('Cancelado', 'Cancelado'),
    ]

    id_compra = models.AutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=20, unique=True) # Conservado como lo pediste
    numero_factura = models.CharField(max_length=50)
    fecha_compra = models.DateTimeField()
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, default='Efectivo')
    estado = models.CharField(max_length=20, choices=ESTADO_COMPRA_CHOICES, default='Recibido')
    total_compra = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    observaciones = models.TextField(blank=True, null=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, db_column='id_proveedor')
    # Doble relación con Usuarios 
    id_usuario_registro = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='compras_registradas', 
        db_column='id_usuario_registro'
    )
    id_usuario_recepcion = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='compras_recibidas', 
        db_column='id_usuario_recepcion',
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

    def __str__(self):
        return f"Compra {self.codigo_interno} - Factura {self.numero_factura}"


class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio_unitario_compra = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    lote = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles', db_column='id_compra')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')

    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compras"