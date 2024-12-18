from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils import timezone
from ..models import RoadTrip, Utilisateur
from datetime import datetime, timedelta, time
from ..services import TransportService


class RoadTripCreateView(CreateView):
    model = RoadTrip
    template_name = 'app_users/roadtrip/create.html'
    fields = ['description', 'publique']
    success_url = reverse_lazy('enregistrements')
    login_url = 'login'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transport_service = TransportService()
        self.object = None

    def get_trips_for_segment(self, depart, arrivee, date, previous_arrival=None):
        """
        Recherche des trajets entre deux villes en tenant compte du trajet précédent
        """
        try:
            if previous_arrival:
                prev_datetime = datetime.strptime(previous_arrival, "%Y%m%dT%H%M%S")
                min_departure = prev_datetime + timedelta(minutes=30)

                if min_departure.date() < date.date():
                    min_departure = datetime.combine(date.date(), time(8, 0))

                heures = []
                current_hour = min_departure
                for _ in range(6):
                    heures.append(current_hour.strftime("%H:%M:%S"))
                    current_hour += timedelta(hours=2)
            else:
                heures = ["08:00:00", "10:00:00", "12:00:00", "14:00:00", "16:00:00", "18:00:00"]

            all_options = []
            for heure in heures:
                datetime_str = f"{date.strftime('%Y-%m-%d')}T{heure}"
                journey_datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")

                try:
                    trips = self.transport_service.reach(
                        start=depart,
                        stop=arrivee,
                        journey_date=journey_datetime
                    )
                    if trips:
                        for trip in trips:
                            # Ne garder que les trajets qui respectent l'heure minimale de départ
                            if not previous_arrival or datetime.strptime(trip[0]['raw_departure'],
                                                                         "%Y%m%dT%H%M%S") >= min_departure:
                                all_options.append(trip)

                except Exception as e:
                    print(f"Erreur pour l'heure {heure}: {str(e)}")
                    continue

            # Trier par prix et prendre les 5 meilleures options
            sorted_options = sorted(all_options, key=lambda x: x[0].get('total_price', float('inf')))
            return sorted_options[:5] if sorted_options else []

        except Exception as e:
            print(f"Erreur lors de la recherche des trajets: {str(e)}")
            return []

    def validate_dates(self, dates):
        """Vérifie que les dates sont chronologiques"""
        for i in range(len(dates) - 1):
            if dates[i] >= dates[i + 1]:
                return False
        return True

    def validate_cities(self, cities):
        """Vérifie que les villes sont différentes les unes des autres"""
        for i in range(len(cities) - 1):
            if cities[i] == cities[i + 1]:
                return False, f"Les villes {cities[i]} et {cities[i + 1]} sont identiques"
        return True, ""

    def get(self, request, *args, **kwargs):
        """Gestion de la page initiale"""
        self.object = None
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """Gère la soumission du formulaire"""
        print("Début de la méthode post")
        print("Action reçue:", request.POST.get('action'))

        form = self.get_form()
        action = request.POST.get('action', '')

        if not form.is_valid():
            print("Formulaire invalide")
            return self.form_invalid(form)

        try:
            user_id = request.session.get('user_id')
            print("User ID:", user_id)

            utilisateur = Utilisateur.objects.get(id=user_id)

            # Récupération des villes
            cities = [
                city for city in [
                    request.POST.get('depart'),
                    request.POST.get('etape1'),
                    request.POST.get('etape2'),
                    request.POST.get('arrivee')
                ] if city and city.strip()
            ]
            print("Villes récupérées:", cities)

            # Validation des villes
            is_valid, error_message = self.validate_cities(cities)
            if not is_valid:
                messages.error(request, error_message)
                return self.form_invalid(form)

            # Récupération des dates
            dates = []
            date_fields = ['depart_date', 'etape1_date', 'etape2_date', 'arrivee_date']
            for i, city in enumerate(cities):
                date_str = request.POST.get(date_fields[i])
                if date_str:
                    dates.append(datetime.strptime(date_str, '%Y-%m-%d'))
            print("Dates récupérées:", dates)

            if not self.validate_dates(dates):
                messages.error(request, "Les dates doivent être chronologiques.")
                return self.form_invalid(form)

            # Traitement selon l'action
            if action == 'search':
                return self._handle_search(request, form, cities, dates, utilisateur)
            elif action == 'confirm':
                return self._handle_confirm(request, form, dates, utilisateur)

        except Utilisateur.DoesNotExist:
            messages.error(request, "Utilisateur non trouvé. Veuillez vous reconnecter.")
            return redirect('login')
        except Exception as e:
            print(f"Erreur inattendue: {str(e)}")
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            return self.form_invalid(form)

        return self.form_invalid(form)

    def _handle_search(self, request, form, cities, dates, utilisateur):
        """Gère la recherche des trajets"""
        print("Démarrage de la recherche de trajets")

        segment_options = []
        previous_arrival = None

        for i in range(len(cities) - 1):
            print(f"\nRecherche pour le segment {i + 1}: {cities[i]} → {cities[i + 1]}")
            current_date = dates[i]

            trips = self.get_trips_for_segment(
                cities[i],
                cities[i + 1],
                current_date,
                previous_arrival
            )

            if not trips:
                error_msg = f"Aucun trajet trouvé entre {cities[i]} et {cities[i + 1]} pour la date {current_date.strftime('%d/%m/%Y')}"
                messages.error(request, error_msg)
                return self.form_invalid(form)

            segment_options.append(trips)

            if trips and trips[0]:
                last_step = trips[0][-1]
                previous_arrival = last_step.get('raw_arrival')

        context = self.get_context_data(
            form=form,
            trips_data={
                'segment_options': segment_options,
                'cities': cities,
                'dates': [d.strftime('%Y-%m-%d') for d in dates],
            }
        )

        return render(request, self.template_name, context)

    def _handle_confirm(self, request, form, dates, utilisateur):
        """Gère la confirmation et création du roadtrip"""
        try:
            # Ajouter une heure spécifique pour éviter les problèmes de timezone
            depart_date = dates[0]
            retour_date = dates[-1]

            depart_time = timezone.make_aware(datetime.combine(depart_date, time(12, 0)))
            retour_time = timezone.make_aware(datetime.combine(retour_date, time(12, 0)))

            roadtrip = RoadTrip.objects.create(
                utilisateur=utilisateur,
                description=form.cleaned_data.get('description', ''),
                publique=form.cleaned_data.get('publique', False),
                depart=depart_time,
                retour=retour_time,
                nom=f"Voyage du {depart_time.strftime('%d/%m/%Y')}",
                nbjour=(retour_date - depart_date).days + 1
            )

            messages.success(request, "Votre Roadtrip a été créé avec succès!")
            return redirect('enregistrements')

        except Exception as e:
            print(f"Erreur lors de la création du roadtrip: {str(e)}")
            messages.error(request, f"Une erreur est survenue lors de la création du roadtrip: {str(e)}")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """Prépare le contexte pour le template"""
        context = super().get_context_data(**kwargs)
        if 'trips_data' in kwargs:
            context['trips_data'] = kwargs['trips_data']
        return context