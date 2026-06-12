from django import forms
from .models import Servicio, ListaServicio

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