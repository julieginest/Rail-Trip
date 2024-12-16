from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms
from django.http import JsonResponse
from datetime import datetime
from ..services import TransportService
from Prix.func import prix
from django.shortcuts import render, redirect
from django.contrib import messages

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Vous avez était déconnecté avec succès.")
    return redirect("login")

# from ...Prix.func import prix

class TrajetForm(forms.Form):
    ville_depart = forms.CharField(max_length=100, required=True, label="Ville de départ")
    ville_arrivee = forms.CharField(max_length=100, required=True, label="Ville d'arrivée")
    jour_depart = forms.DateField(required=True, label="Date de départ", widget=forms.SelectDateWidget())
    heure_depart = forms.TimeField(
        required=True,
        label="Heure de départ",
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial='09:00'
    )
    
class HomeView(TemplateView):
    template_name = "app_trips/home.html"

    def get_real_trips(self, ville_depart, ville_arrivee, jour_depart):
        """Obtient les trajets réels via l'API de transport"""
        try:
            transport_service = TransportService()
            api_response = transport_service.reach(
                start=ville_depart,
                stop=ville_arrivee,
                journey_date=jour_depart
            )

            # Formatage des résultats de l'API
            trips = []
            if 'journeys' in api_response:
                for journey in api_response['journeys']:
                    departure = datetime.strptime(journey['departure_date_time'], "%Y%m%dT%H%M%S")
                    arrival = datetime.strptime(journey['arrival_date_time'], "%Y%m%dT%H%M%S")
                    
                    # Extraction des informations nécessaires pour le prix
                    #distance = journey.get('distance', 0) / 1000.0  # Convertir en km
                    #network = journey.get('sections', [{}])[0].get('display_informations', {}).get('network', "Unknown")

                    # # Calcul du prix en utilisant la fonction prix
                    price = 0
                    for p in journey["sections"]:
                        if (p["type"] == "public_transport"):
                            price = price + prix(p["geojson"]["properties"][0]["length"] / 1000, p["departure_date_time"], p["display_informations"]["network"])

                    
                    trip = {
                        "name": f"Trajet {ville_depart} - {ville_arrivee}",
                        "start_location": ville_depart,
                        "end_location": ville_arrivee,
                        "description": self._get_journey_description(journey),
                        "date": departure.strftime("%Y-%m-%d"),
                        "start_hour": departure.strftime("%H:%M"),
                        "end_hour": arrival.strftime("%H:%M"),
                        "duration": self._format_duration(journey.get('duration', 0) // 60 ), 
                        "price": round(price,2) ,
                        #"train_type": network              
                        }
                    trips.append(trip)

            return trips
        except Exception as e:
            print(f"Erreur API (from home): {str(e)}")
            # En cas d'erreur, on retourne les trajets fictifs
            return get_fake_roadtrips(ville_depart, ville_arrivee, jour_depart)
        
    def _format_duration(self, duration_minutes):
        if duration_minutes <= 0:
            return "Durée inconnue"
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}min" if minutes > 0 else f"{hours}h"
        return f"{minutes}min"

    def _get_journey_description(self, journey):
        """Génère une description du trajet basée sur les sections"""
        sections = []
        for section in journey.get('sections', []):
            if section.get('type') == 'public_transport':
                info = section.get('display_informations', {})
                sections.append(f"Train {info.get('headsign', '')} - {info.get('network', '')}")

        return " → ".join(sections) if sections else "Trajet direct"

    def get(self, request, *args, **kwargs):
        form = TrajetForm()
        context = {
            'form': form,
            'roadtrips': []  # Aucun trajet n'est affiché initialement
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = TrajetForm(request.POST)

        if form.is_valid():
            ville_depart = form.cleaned_data['ville_depart']
            ville_arrivee = form.cleaned_data['ville_arrivee']
            jour_depart = form.cleaned_data['jour_depart']
            heure_depart = form.cleaned_data['heure_depart']

            # Combinaison de la date et de l'heure
            date_heure_depart = datetime.combine(jour_depart, heure_depart)

            # Obtenir uniquement les trajets réels via l'API
            roadtrips = self.get_real_trips(ville_depart, ville_arrivee, date_heure_depart)
        else:
            roadtrips = []

        context = {
            'form': form,
            'roadtrips': roadtrips
        }
        return self.render_to_response(context)
