from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms
from django.http import JsonResponse
from datetime import datetime
from ..services import TransportService
from django.shortcuts import render, redirect
from django.contrib import messages

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Vous avez était déconnecté avec succès.")
    return redirect("login")

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

    def format_trips_for_display(self, sanitized_trips):
        """Formate les trajets sanitizés pour l'affichage"""
        formatted_trips = []
        
        for journey in sanitized_trips:
            if journey:  # Vérifie si le trajet contient des étapes
                first_step = journey[0]
                last_step = journey[-1]
                
                total_price = sum(step['price'] for step in journey)
                
                # Calcul de la durée totale
                departure = datetime.strptime(first_step['departure_date_time'], "%Y%m%dT%H%M%S")
                arrival = datetime.strptime(last_step['arrival_date_time'], "%Y%m%dT%H%M%S")
                duration_minutes = int((arrival - departure).total_seconds() / 60)

                trip = {
                    "name": f"Trajet {first_step['from']} - {last_step['to']}",
                    "start_location": first_step['from'],
                    "end_location": last_step['to'],
                    "description": self._get_journey_description(journey),
                    "date": departure.strftime("%Y-%m-%d"),
                    "start_hour": departure.strftime("%H:%M"),
                    "end_hour": arrival.strftime("%H:%M"),
                    "duration": self._format_duration(duration_minutes),
                    "price": round(total_price, 2)
                }
                formatted_trips.append(trip)
                
        return formatted_trips

    def _format_duration(self, duration_minutes):
        if duration_minutes <= 0:
            return "Durée inconnue"
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}min" if minutes > 0 else f"{hours}h"
        return f"{minutes}min"

    def _get_journey_description(self, journey):
        """Génère une description du trajet basée sur les étapes sanitizées"""
        descriptions = []
        for step in journey:
            if step['type'] == 'public_transport':
                descriptions.append(f"Train {step['network']}")
        
        return " → ".join(descriptions) if descriptions else "Trajet direct"

    def get(self, request, *args, **kwargs):
        form = TrajetForm()
        context = {
            'form': form,
            'roadtrips': []
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = TrajetForm(request.POST)

        if form.is_valid():
            ville_depart = form.cleaned_data['ville_depart']
            ville_arrivee = form.cleaned_data['ville_arrivee']
            jour_depart = form.cleaned_data['jour_depart']
            heure_depart = form.cleaned_data['heure_depart']

            date_heure_depart = datetime.combine(jour_depart, heure_depart)

            try:
                transport_service = TransportService()
                sanitized_trips = transport_service.reach(
                    start=ville_depart,
                    stop=ville_arrivee,
                    journey_date=date_heure_depart
                )
                
                roadtrips = self.format_trips_for_display(sanitized_trips)
            except Exception as e:
                print(f"Erreur lors de la recherche des trajets: {str(e)}")
                messages.error(request, "Erreur lors de la recherche des trajets.")
                roadtrips = []
        else:
            roadtrips = []

        context = {
            'form': form,
            'roadtrips': roadtrips
        }
        return self.render_to_response(context)
