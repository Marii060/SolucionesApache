from django import forms
from django.forms import inlineformset_factory
from .models import Categoria, MarcaProducto, Fabricante, Producto, Proveedor,Compra, DetalleCompra

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

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social', 'nombre', 'identificacion', 'activo', 'telefono', 'correo', 'direccion']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Motopartes S.A.'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Motopartes (Nombre Comercial)'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 900.123.456-7'}),
            'activo': forms.Select(choices=[(True, 'Activo'), (False, 'Inactivo')], attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 601 555 0001'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ventas@proveedor.com'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Calle 80 #23-45, Bogotá'}),
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
        
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = [
            'codigo_interno', 'numero_factura', 'fecha_compra', 
            'id_proveedor', 'metodo_pago', 'estado', 'estado_pago', 
            'observaciones', 'total_compra'
        ]
        widgets = {
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: OC-001'}),
            'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: F-98765'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'id_proveedor': forms.Select(attrs={'class': 'form-select'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'estado_pago': forms.Select(attrs={'class': 'form-select'}),
            'total_compra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }
        
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['id_producto', 'cantidad', 'precio_unitario_compra', 'subtotal']
        widgets = {
            'id_producto': forms.Select(attrs={'class': 'form-select producto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input', 'min': '1'}),
            'precio_unitario_compra': forms.NumberInput(attrs={'class': 'form-control precio-input'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control subtotal-input', 'readonly': 'readonly'}),
        }

# Fábrica para manejar el encabezado y sus detalles juntos
CompraFormSet = inlineformset_factory(
    Compra, 
    DetalleCompra, 
    form=DetalleCompraForm, 
    extra=1, # Cantidad de filas vacías iniciales
    can_delete=True
)        