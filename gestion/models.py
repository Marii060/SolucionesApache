from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula de Extranjería'),
    ]
    
    id_cliente = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES, default='CC')
    nombre = models.CharField(max_length=100, default='Por definir')
    numero_documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razon_social

class Moto(models.Model):
    id_moto = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=15, unique=True)
    marca = models.CharField(max_length=40)
    modelo = models.CharField(max_length=40)
    cilindraje = models.CharField(max_length=30)
    kilometraje = models.CharField(max_length=30, null=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')

    def __str__(self):
        return f"{self.placa} - {self.modelo}"
    
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuarios"

    def __str__(self):
        return self.nombre

class Log(models.Model):
    id_log = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(auto_now_add=True) # Django pone la fecha y hora automáticamente
    accion_realizada = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        verbose_name = "Registro de Sistema (Log)"
        verbose_name_plural = "Registros de Sistema (Logs)"

    def __str__(self):
        return f"{self.fecha_hora} - {self.id_usuario.username}: {self.accion_realizada}"    