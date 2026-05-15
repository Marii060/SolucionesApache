from django.db import models

class MarcaProducto(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    codigo_interno = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

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
        return self.razon_social

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
    # Esta es la relacion de muchos a muchos de productos con proveedores
    proveedores = models.ManyToManyField(Proveedor, related_name='productos')

    def __str__(self):
        return self.nombre