from django import forms
from django.core.exceptions import ValidationError
from .models import Cliente, Moto

# Definimos solo las dos opciones necesarias
TIPO_RAZON_SOCIAL = [
    ('', 'Seleccione tipo (Opcional)'), # Opción vacía para que sea opcional
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
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1098765432'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del cliente'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 3101234567'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aquí hacemos que el campo sea opcional
        self.fields['razon_social'].required = False
        
        # Opcional: Si quieres asegurarte de que 'nombre' no tenga valores iniciales extraños:
        self.fields['nombre'].initial = ''
    
def clean_numero_documento(self):
        documento = self.cleaned_data.get('numero_documento')
        
        # Buscamos si existe otro cliente con ese mismo documento
        # 'exclude(pk=self.instance.pk)' es importante para que 
        # al editar un cliente no nos marque error a nosotros mismos
        if Cliente.objects.filter(numero_documento=documento).exclude(pk=self.instance.pk).exists():
            raise ValidationError("¡Atención! Este número de documento ya se encuentra registrado.")
        
        return documento
        
class MotoForm(forms.ModelForm):
    class Meta:
        model = Moto
        fields = ['placa', 'marca', 'modelo', 'cilindraje', 'kilometraje']
        
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ABC-123'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Honda'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. CB500F'}),
            'cilindraje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 471 cc'}),
            'kilometraje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 23500 km'}),
        }        
def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        # Buscamos si existe otra moto con esa misma placa
        if Moto.objects.filter(placa=placa).exists():
            raise ValidationError("¡Atención! Ya existe una moto registrada con esta placa.")
        return placa