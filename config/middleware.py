from django.shortcuts import redirect

class RestringirAccesoAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Rutas que quieres prohibir para el superusuario
        rutas_prohibidas = ['/gestion/', '/operaciones/', '/inventario/']
        
        # Comprobamos si el usuario es superusuario
        if request.user.is_authenticated and request.user.is_superuser:
            # Revisamos si la ruta actual empieza con alguna de las prohibidas
            if any(request.path.startswith(ruta) for ruta in rutas_prohibidas):
                # Si intenta entrar, lo mandamos de vuelta al admin
                return redirect('/admin/') 
        
        response = self.get_response(request)
        return response