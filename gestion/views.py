from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Moto
from .forms import ClienteForm 

@login_required
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_motos = Moto.objects.count() 
    
    contexto = {
        'total_clientes': total_clientes,
        'total_motos': total_motos,
    }
    return render(request, 'gestion/dashboard.html', contexto)

@login_required 
def lista_clientes(request):
    clientes = Cliente.objects.all()   
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})

@login_required
def crear_cliente(request):
    # Si el usuario le dio clic al botón "Guardar" en el formulario...
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save() # Guardamos en la base de datos
            messages.success(request, '¡Cliente guardado exitosamente en Soluciones Apache!')
            return redirect('gestion:lista_clientes') # Lo devolvemos a la tabla
    
    # Si solo entró a ver la página en blanco...
    else:
        form = ClienteForm()
        
    return render(request, 'gestion/crear_cliente.html', {'form': form})