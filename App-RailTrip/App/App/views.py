from django.shortcuts import render

# Page d'accueil
def home(request):
    return render(request, 'home.html')

# Page de résultats de recherche
def search(request):
    # Simulation pour l'instant
    voyages = [
        {'depart': 'Paris', 'arrive': 'Lyon'},
        {'depart': 'Marseille', 'arrive': 'Nice'},
    ]
    return render(request, 'home.html', {'voyages': voyages})
