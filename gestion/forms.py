from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['tipo_documento', 'numero_documento', 'razon_social', 'nombre', 'correo', 'telefono', 'direccion']
        
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1098765432'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional (Solo para empresas)'}),
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