from django import forms
from .models import Cliente

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