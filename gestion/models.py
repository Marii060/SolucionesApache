from django.db import models

class Cliente(models.Model):
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula de Extranjería'),
    ]
    
    id_cliente = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=150)
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES, default='CC')
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