from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Moto, User, ConfiguracionSistema

# Definimos solo las dos opciones necesarias
TIPO_RAZON_SOCIAL = [
    ('', 'Seleccione tipo (Opcional)'), 
    ('natural', 'Persona Natural'),
    ('juridica', 'Persona Jurídica'),
]

class ClienteForm(forms.ModelForm):
    # Definimos el campo como ChoiceField para el desplegable
    razon_social = forms.ChoiceField(
        choices=TIPO_RAZON_SOCIAL, 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Cliente
        fields = ['tipo_documento', 'numero_documento', 'razon_social', 'nombre', 'correo', 'telefono', 'direccion']
        
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            # Cambiamos a NumberInput para forzar números y agregamos required: True
            'numero_documento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1098765432', 'required': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del cliente'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            # Cambiamos a NumberInput para forzar números y agregamos required: True
            'telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 3101234567', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['razon_social'].required = False
        self.fields['nombre'].initial = ''
    
    def clean_numero_documento(self):
        documento = self.cleaned_data.get('numero_documento')
        
        # Validamos que solo sean números (por si intentan saltarse el navegador)
        if documento and not str(documento).isdigit():
            raise ValidationError("El documento solo debe contener números.")

        # Buscamos si existe otro cliente con ese mismo documento
        if Cliente.objects.filter(numero_documento=documento).exclude(pk=self.instance.pk).exists():
            raise ValidationError("¡Atención! Este número de documento ya se encuentra registrado.")
        
        return documento

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        
        # Validamos que solo sean números
        if telefono and not str(telefono).isdigit():
            raise ValidationError("El teléfono solo debe contener números.")
            
        return telefono
        
class MotoForm(forms.ModelForm):
    id_cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        empty_label="Seleccione un cliente...",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = Moto
        fields = ['id_cliente','placa', 'marca', 'modelo', 'cilindraje', 'kilometraje', 'observaciones']
        labels = {
            'id_cliente': 'Cliente', 
        }
        widgets = {
            'id_cliente': forms.Select(attrs={'class': 'form-select'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ABC-123'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Honda'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. CB500F'}),
            'cilindraje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 471 cc'}),
            'kilometraje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 23500 km'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ej. Estado general, modificaciones, detalles a tener en cuenta...'}),
        }        
def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        # Buscamos si existe otra moto con esa misma placa
        if Moto.objects.filter(placa=placa).exists():
            raise ValidationError("¡Atención! Ya existe una moto registrada con esta placa.")
        return placa
    
class ConfiguracionSistemaForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionSistema
        fields = [
            'tipo_documento', 'nit', 'razon_social', 'telefono', 'email', 'direccion',
            'iva_porcentaje', 'moneda_simbolo', 'moneda_nombre', 'stock_minimo_alerta', 
            'dias_credito_default', 'maneja_iva', 'resolucion_dian', 'prefijo_factura',
        ]
        
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'maneja_iva': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'iva_porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), 
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Aplicamos 'form-control' a todo, MENOS al select y al checkbox
            if field_name != 'tipo_documento' and field_name != 'maneja_iva':
                field.widget.attrs.update({'class': 'form-control'})