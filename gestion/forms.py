from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        # Le decimos a Django qué campos de la base de datos queremos mostrar en pantalla
        fields = ['tipo_documento', 'numero_documento', 'razon_social', 'nombre', 'correo', 'telefono', 'direccion']
        
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1098765432'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Solo para empresas (opcional)'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 3101234567'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }