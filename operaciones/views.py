from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ServicioForm

@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            # form.save(commit=False) prepara los datos pero pausa el guardado en la BD
            servicio = form.save(commit=False) 
            
            # Asignamos automáticamente el usuario que tiene la sesión iniciada
            servicio.id_usuario = request.user 
            
            # Ahora sí, guardamos definitivamente en MySQL
            servicio.save() 
            
            messages.success(request, '¡Orden de servicio creada con éxito!')
            return redirect('operaciones:lista_servicios') # Ajusta el nombre de tu URL si es diferente
    else:
        form = ServicioForm()
        
    return render(request, 'operaciones/registrar_servicio.html', {'form': form})
