from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['codigo_interno', 'nombre', 'descripcion', 'estado']
        widgets = {
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CAT-001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lubricantes, Repuestos, Accesorios...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descripción...'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }