from django import forms
from .models import Servicio, ListaServicio, Venta, CreditoPagado

class ListaServicioForm(forms.ModelForm):
    class Meta:
        model = ListaServicio
        fields = ['nombre_servicio', 'precio_base_mano_obra', 'estado', 'descripcion']
        labels = {
            'nombre_servicio': 'Nombre Servicio',
            'precio_base_mano_obra': 'Precio Base Mano Obra',
            'estado': 'Estado',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mantenimiento General'}),
            'precio_base_mano_obra': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'transform: scale(1.5); margin-top: 6px;'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['codigo_servicio', 'id_moto', 'mecanico', 'descripcion', 'estado']
        labels = {
            'codigo_servicio': 'Código de la Orden (Ej: ORD-001)',
            'id_moto': 'Seleccione la Moto (Placa)',
            'mecanico': 'Mecánico Asignado',
            'descripcion': 'Descripción de la Falla / Motivo de Ingreso',
            'estado': 'Estado Inicial',
        }
        widgets = {
            'codigo_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'id_moto': forms.Select(attrs={'class': 'form-select'}),
            'mecanico': forms.TextInput(attrs={'class': 'form-control'}), 
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class VentaForm(forms.ModelForm):
    # Definimos las opciones estáticas para el tipo de pago
    OPCIONES_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Credito', 'Crédito'),
    ]
    
    # Sobrescribimos el campo para que sea un select desplegable
    tipo_pago = forms.ChoiceField(
        choices=OPCIONES_PAGO, 
        widget=forms.Select(attrs={'class': 'form-select', 'required': True})
    )

    class Meta:
        model = Venta
        # Solo le pedimos al usuario los datos que realmente necesita ingresar
        fields = ['id_cliente', 'tipo_pago', 'observacion']
        
        # Le aplicamos las clases de Bootstrap para que se vea moderno
        widgets = {
            'id_cliente': forms.Select(attrs={
                'class': 'form-select', 
                'required': True
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2, 
                'placeholder': 'Escribe aquí si hay alguna nota adicional sobre esta venta...'
            }),
        }
        
        labels = {
            'id_cliente': 'Seleccionar Cliente',
            'tipo_pago': 'Método de Pago',
            'observacion': 'Observaciones (Opcional)',
        }        
        

class AbonoForm(forms.ModelForm):
    class Meta:
        model = CreditoPagado
        fields = ['monto_pago', 'metodo_pago']
        widgets = {
            'monto_pago': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: 50000',
                'min': '1'
            }),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('Efectivo', 'Efectivo'),
                ('Transferencia', 'Transferencia'),
            ]),
        }
        labels = {
            'monto_pago': 'Monto a abonar ($)',
            'metodo_pago': 'Método de pago',
        }        