from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        # Solo pedimos lo necesario para abrir la orden
        fields = ['codigo_servicio', 'id_moto', 'descripcion', 'estado']
        labels = {
            'codigo_servicio': 'Código de la Orden (Ej: ORD-001)',
            'id_moto': 'Seleccione la Moto (Placa)',
            'descripcion': 'Descripción de la Falla / Motivo de Ingreso',
            'estado': 'Estado Inicial',
        }
        widgets = {
            'codigo_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'id_moto': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }