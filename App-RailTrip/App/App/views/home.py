# views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms

# Données fictives pour simuler des trajets
def get_fake_roadtrips(ville_depart=None, ville_arrivee=None, jour_depart=None):
    roadtrips = [
        {
            "name": "Road Trip Paris - Lyon",
            "start_location": "Paris Gare de Lyon",
            "end_location": "Lyon Part-Dieu",
            "description": "Un road trip magnifique à travers la France, de la capitale Paris à la ville de Lyon.",
            "date": "2024-12-01",
            "start_hour": "10h00",
            "end_hour": "12h00"
        },
        {
            "name": "Road Trip Lyon - Marseille",
            "start_location": "Lyon Part-Dieu",
            "end_location": "Marseille Saint-Charles",
            "description": "Découvrez les magnifiques paysages entre Lyon et Marseille, en passant par les montagnes.",
            "date": "2024-12-10",
            "start_hour": "10h00",
            "end_hour": "12h00"
        },
        {
            "name": "Road Trip Toulouse - Bordeaux",
            "start_location": "Toulouse Matabiau",
            "end_location": "Bordeaux Saint-Jean",
            "description": "Parcourez le sud-ouest de la France, avec des arrêts dans les célèbres vignobles bordelais.",
            "date": "2024-12-15",
            "start_hour": "10h00",
            "end_hour": "12h00"
        }
    ]
    
    # Filtrage des trajets en fonction des critères
    if ville_depart:
        roadtrips = [trip for trip in roadtrips if ville_depart.lower() in trip["start_location"].lower()]
    if ville_arrivee:
        roadtrips = [trip for trip in roadtrips if ville_arrivee.lower() in trip["end_location"].lower()]
    if jour_depart:
        # Convertir jour_depart en chaîne au format 'YYYY-MM-DD'
        jour_depart_str = jour_depart.strftime("%Y-%m-%d")
        roadtrips = [trip for trip in roadtrips if jour_depart_str == trip["date"]]
    
    return roadtrips

# Formulaire de recherche
class TrajetForm(forms.Form):
    ville_depart = forms.CharField(max_length=100, required=False, label="Ville de départ")
    ville_arrivee = forms.CharField(max_length=100, required=False, label="Ville d'arrivée")
    jour_depart = forms.DateField(required=False, label="Date de départ", widget=forms.SelectDateWidget())

# Vue pour la page d'accueil
class HomeView(TemplateView):
    template_name = "app_trips/home.html"

    def get(self, request, *args, **kwargs):
        form = TrajetForm()

        # Récupérer les roadtrips (sans filtre initialement)
        roadtrips = get_fake_roadtrips()

        context = {
            'form': form,  # Passer le formulaire au template
            'roadtrips': roadtrips  # Passer la liste des roadtrips au template
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = TrajetForm(request.POST)

        roadtrips = []
        if form.is_valid():
            ville_depart = form.cleaned_data.get('ville_depart')
            ville_arrivee = form.cleaned_data.get('ville_arrivee')
            jour_depart = form.cleaned_data.get('jour_depart')

            # Récupérer les trajets filtrés en fonction des critères
            roadtrips = get_fake_roadtrips(ville_depart=ville_depart, ville_arrivee=ville_arrivee, jour_depart=jour_depart)

        context = {
            'form': form,
            'roadtrips': roadtrips  # Passer les roadtrips filtrés au template
        }
        return self.render_to_response(context)
