from django.db import models
from django.core.cache import cache
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
    
    @property
    def ultimo_servicio(self):
        return self.servicio_set.order_by('-fecha_inicio').first()
    def __str__(self):
        return f"{self.placa} - {self.modelo}"

class Log(models.Model):
    id_log = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(auto_now_add=True, db_column='fecha_hora') # Mapeo explícito
    accion_realizada = models.CharField(max_length=100, db_column='accion_realizada')
    descripcion = models.CharField(max_length=100, blank=True, null=True, db_column='descripcion')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'log' 
        verbose_name = "Registro de Sistema (Log)"
        verbose_name_plural = "Registros de Sistema (Logs)"

    def __str__(self):
        return f"{self.fecha_hora} - {self.id_usuario.username}: {self.accion_realizada}"

class ConfiguracionSistema(models.Model):
    TIPO_DOC_CHOICES = [
        ('recibo', 'Recibo de venta (sin DIAN)'),
        ('factura', 'Factura electrónica (con DIAN)'),
    ]

    id = models.AutoField(primary_key=True)
    
    #DATOS DEL TALLER
    tipo_documento = models.CharField(
        max_length=20, 
        choices=TIPO_DOC_CHOICES, 
        default='recibo', 
        verbose_name="Tipo Documento"
    )
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT / Documento")
    razon_social = models.CharField(max_length=100, verbose_name="Razón Social")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Email de Contacto")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    
    #PARÁMETROS DEL SISTEMA
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=19.00, verbose_name="IVA (%)")
    moneda_simbolo = models.CharField(max_length=5, default='$', verbose_name="Símbolo Moneda")
    moneda_nombre = models.CharField(max_length=20, default='COP', verbose_name="Nombre Moneda")
    stock_minimo_alerta = models.PositiveIntegerField(default=5, verbose_name="Stock Mínimo Alerta")
    dias_credito_default = models.PositiveIntegerField(default=30, verbose_name="Días Crédito (Defecto)")
    
    #COPIAS DE SEGURIDAD
    backup_automatico_activo = models.BooleanField(default=False, verbose_name="Backup Automático Activo")
    ultima_copia_seguridad = models.DateTimeField(null=True, blank=True, verbose_name="Última Copia Realizada")

    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"

    def __str__(self):
        return f"Configuración del Sistema - {self.razon_social}"

    # Singleton para asegurar que solo exista un registro
    def save(self, *args, **kwargs):
        # Asegura que siempre se guarde con ID=1
        self.id = 1
        super().save(*args, **kwargs)
        # Limpia el cache al guardar
        cache.delete('configuracion_sistema')

    @classmethod
    def obtener_config(cls):
        # Implementación con Cache para máximo rendimiento
        config = cache.get('configuracion_sistema')
        if not config:
            # Si no está en cache, lo busca en la BD, creándolo si no existe
            config, created = cls.objects.get_or_create(id=1, defaults={
                'razon_social': 'Soluciones Apache', 
                'nit': '000000000-0',
                'tipo_documento': 'recibo', 
            })
            # Cache por 24 horas
            cache.set('configuracion_sistema', config, 86400) 
        return config