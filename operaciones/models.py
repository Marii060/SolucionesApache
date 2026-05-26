from django.db import models
from django.contrib.auth.models import User
from gestion.models import Moto
from inventario.models import Producto

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