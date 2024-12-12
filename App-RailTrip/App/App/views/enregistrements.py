# enregistrements.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def enregistrements(request):
    if request.user.is_authenticated:
        # Logique pour récupérer les enregistrements de l'utilisateur
        return render(request, 'enregistrements.html', {'enregistrements': enregistrements})
    else:
        return redirect('login')