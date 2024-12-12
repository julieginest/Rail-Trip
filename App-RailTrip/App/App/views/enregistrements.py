from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import RoadTrip

def enregistrements(request):
    utilisateur = request.user
    roadtrips = RoadTrip.objects.filter(utilisateur=utilisateur) 
    return render(request, 'enregistrement.html', {'roadtrips': roadtrips})
