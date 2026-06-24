from django import forms
from .models import Categoria, MarcaProducto, Fabricante, Producto

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
        
class MarcaForm(forms.ModelForm):
    class Meta:
        model = MarcaProducto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Yamaha, Motul, Brembo...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Breve descripción de la marca...'}),
        }        
        
class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Yamaha, Honda, Bajaj...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción o información de contacto del fabricante (Opcional)...'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo_interno', 'codigo_barras', 'nombre', 'id_categoria', 'id_marca',
            'id_fabricante', # <-- Agregamos el campo aquí
            'descripcion', 'precio_compra', 'precio_venta', 'stock_minimo', 'cantidad',
            'disponible', 'proveedores'
        ]
        widgets = {
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PRD-001'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional...'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del repuesto o artículo...'}),
            'id_categoria': forms.Select(attrs={'class': 'form-select'}),
            'id_marca': forms.Select(attrs={'class': 'form-select'}),
            'id_fabricante': forms.Select(attrs={'class': 'form-select'}), # <-- Le damos estilo de Bootstrap aquí
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Detalles técnicos o aplicación...'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'proveedores': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedores'].required = False