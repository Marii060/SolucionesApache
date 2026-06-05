from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula de Extranjería'),
    ]
    
    id_cliente = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=20, blank=True, null=True)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES, default='CC')
    nombre = models.CharField(max_length=100, default='Por definir')
    numero_documento = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero_documento} - {self.nombre}"

class Moto(models.Model):
    id_moto = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=15, unique=True)
    marca = models.CharField(max_length=40)
    modelo = models.CharField(max_length=40)
    cilindraje = models.CharField(max_length=30)
    kilometraje = models.CharField(max_length=30, null=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    observaciones = models.TextField(null=True, blank=True)
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

     
class Empleado(models.Model):
    # Esto conecta este perfil con el usuario de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Esto conecta el empleado con el rol que creaste anteriormente
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    
    telefono = models.CharField(max_length=20, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Empleado del Taller"
        verbose_name_plural = "Empleados del Taller"

    def __str__(self):
        return f"{self.user.username} - {self.rol}"    
    
class Rol(models.Model):
    # Opciones: Administrador, Mecánico, Vendedor
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    estado = models.BooleanField(default=True) # Toggle para activar/desactivar acceso

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.rol}"    