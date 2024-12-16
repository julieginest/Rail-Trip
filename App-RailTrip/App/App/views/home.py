# views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms
from django.http import JsonResponse
from datetime import datetime
from ..services import TransportService
from Prix.func import prix

# from ...Prix.func import prix

def get_fake_roadtrips(ville_depart=None, ville_arrivee=None, jour_depart=None):
    """
    Génère des trajets fictifs pour simulation.

    Args:
        ville_depart (str, optional): Ville de départ pour le filtrage
        ville_arrivee (str, optional): Ville d'arrivée pour le filtrage
        jour_depart (date, optional): Date de départ pour le filtrage

    Returns:
        list: Liste des trajets correspondant aux critères
    """
    roadtrips = [
        {
            "name": "Paris - Lyon",
            "start_location": "Paris Gare de Lyon",
            "end_location": "Lyon Part-Dieu",
            "description": "TGV INOUI - Trajet direct",
            "date": "2024-12-10",
            "start_hour": "08h00",
            "end_hour": "10h00",
            "duration": 120,
            "price": "69€",
            "train_type": "TGV INOUI"
        },
        {
            "name": "Lyon - Marseille",
            "start_location": "Lyon Part-Dieu",
            "end_location": "Marseille Saint-Charles",
            "description": "TGV INOUI - Trajet avec arrêt à Avignon",
            "date": "2024-12-10",
            "start_hour": "10h30",
            "end_hour": "12h45",
            "duration": 135,
            "price": "45€",
            "train_type": "TGV INOUI"
        },
        {
            "name": "Paris - Bordeaux",
            "start_location": "Paris Montparnasse",
            "end_location": "Bordeaux Saint-Jean",
            "description": "TGV INOUI - Trajet direct",
            "date": "2024-12-10",
            "start_hour": "09h00",
            "end_hour": "11h15",
            "duration": 135,
            "price": "79€",
            "train_type": "TGV INOUI"
        },
        {
            "name": "Marseille - Nice",
            "start_location": "Marseille Saint-Charles",
            "end_location": "Nice Ville",
            "description": "TER - Trajet côtier",
            "date": "2024-12-10",
            "start_hour": "13h00",
            "end_hour": "15h30",
            "duration": 150,
            "price": "35€",
            "train_type": "TER"
        },
        {
            "name": "Paris - Lille",
            "start_location": "Paris Nord",
            "end_location": "Lille Flandres",
            "description": "TGV INOUI - Trajet direct",
            "date": "2024-12-10",
            "start_hour": "07h30",
            "end_hour": "08h45",
            "duration": 75,
            "price": "39€",
            "train_type": "TGV INOUI"
        }
    ]

    # Filtrage des trajets
    filtered_trips = roadtrips.copy()

    if ville_depart:
        ville_depart = ville_depart.lower().strip()
        filtered_trips = [
            trip for trip in filtered_trips
            if ville_depart in trip["start_location"].lower()
        ]

    if ville_arrivee:
        ville_arrivee = ville_arrivee.lower().strip()
        filtered_trips = [
            trip for trip in filtered_trips
            if ville_arrivee in trip["end_location"].lower()
        ]

    if jour_depart:
        jour_depart_str = jour_depart.strftime("%Y-%m-%d")
        filtered_trips = [
            trip for trip in filtered_trips
            if jour_depart_str == trip["date"]
        ]

    # Tri des résultats par heure de départ
    filtered_trips.sort(key=lambda x: x["start_hour"])

    return filtered_trips

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
        roadtrips = get_fake_roadtrips()  # Données initiales

        context = {
            'form': form,
            'roadtrips': roadtrips
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

            # Essayer d'obtenir les vrais trajets via l'API
            roadtrips = self.get_real_trips(ville_depart, ville_arrivee, date_heure_depart)

            if not roadtrips:
                roadtrips = get_fake_roadtrips(
                    ville_depart=ville_depart,
                    ville_arrivee=ville_arrivee,
                    jour_depart=date_heure_depart
                )
        else:
            roadtrips = []

        context = {
            'form': form,
            'roadtrips': roadtrips
        }
        return self.render_to_response(context)