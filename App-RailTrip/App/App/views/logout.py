from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')  # 'home' doit correspondre au nom de l'URL de la page d'accueil
