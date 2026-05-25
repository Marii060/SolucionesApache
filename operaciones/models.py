from django.db import models
from django.contrib.auth.models import User
from gestion.models import Moto

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
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    descripcion = models.TextField(blank=True, null=True)
    
    
    id_moto = models.ForeignKey(Moto, on_delete=models.CASCADE, db_column='id_moto')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"Servicio {self.codigo_servicio} - {self.id_moto.placa}"