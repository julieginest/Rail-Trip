from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from .models import Utilisateur

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        exempt_urls = ['/login/', '/register/']
        if request.path in exempt_urls:
            return None

        # Vérifier si l'utilisateur est authentifié
        user_id = request.session.get('user_id')
        if user_id:
            try:
                request.user = Utilisateur.objects.get(id=user_id)
            except Utilisateur.DoesNotExist:
                del request.session['user_id']
                request.user = None
        else:
            request.user = None

        if not request.user and request.path not in exempt_urls:
            return redirect('login')

        return None