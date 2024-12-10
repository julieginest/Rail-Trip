import os
from django.conf import settings
from datetime import date
import requests
import urllib.parse as url
import json
import time
import random


class TransportService:
    API_KEY = "e49dbfec-a940-407b-b845-49c8fe8439b5"
    API_LINK = "https://api.sncf.com/v1/coverage/sncf"

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        ]

    def find_station(self, city_name):
        """
        Trouve l'ID de la gare pour une ville donnée
        """
        auth_args = (self.API_KEY, '')
        # Recherche des gares dans la ville
        search_url = f"{self.API_LINK}/places?q={url.quote(city_name)}&type[]=stop_area"

        response = requests.get(search_url, auth=auth_args)

        if response.status_code != 200:
            raise Exception(f"Erreur lors de la recherche de la gare: {response.text}")

        data = json.loads(response.text)
        if not data.get('places'):
            raise Exception(f"Aucune gare trouvée pour: {city_name}")

        # Cherche d'abord une gare principale
        for place in data['places']:
            if 'gare' in place['name'].lower():
                return place['id']

        # Sinon retourne le premier arrêt trouvé
        return data['places'][0]['id']

    def reach(self, start, stop, journey_date=None, date_use='departure'):
        """
        Recherche des trajets entre deux villes
        """
        try:
            # Trouve les IDs des gares
            start_id = self.find_station(start)
            stop_id = self.find_station(stop)

            print(f"Gare départ ID: {start_id}")
            print(f"Gare arrivée ID: {stop_id}")

            auth_args = (self.API_KEY, '')
            journey_date = journey_date or date.today()

            # Construction du lien avec les IDs des gares
            link = self.build_link(start_id, stop_id, journey_date, date_use)
            print(f"URL de requête: {link}")

            response = requests.get(link, auth=auth_args)

            if response.status_code == 200:
                return json.loads(response.text)
            else:
                print(f"Réponse de l'API: {response.text}")
                raise Exception(f"Erreur API: {response.status_code}")

        except Exception as e:
            raise Exception(f"Erreur lors de la recherche du trajet: {str(e)}")

    def build_link(self, start_id, stop_id, date_obj, date_use):
        """
        Construit l'URL pour l'API SNCF
        """
        date_str = date_obj.strftime("%Y%m%dT%H%M%S")
        return (f"{self.API_LINK}/journeys?"
                f"from={start_id}&"
                f"to={stop_id}&"
                f"datetime={date_str}&"
                f"datetime_represents={date_use}&"
                f"count=5&"  # Nombre de résultats souhaités
                f"min_nb_journeys=3")  # Nombre minimum de trajets

    def get_station_details(self, station_id):
        """
        Récupère les détails d'une gare à partir de son ID
        """
        auth_args = (self.API_KEY, '')
        url = f"{self.API_LINK}/stop_areas/{station_id}"

        response = requests.get(url, auth=auth_args)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data.get('stop_areas', [{}])[0]
        return None

    def format_journey_response(self, api_response, start_name, stop_name):
        """
        Formate la réponse de l'API en un format plus utilisable
        """
        journeys = []

        for journey in api_response.get('journeys', []):
            sections = journey.get('sections', [])
            train_sections = [s for s in sections if s.get('type') == 'public_transport']

            if train_sections:
                first_section = train_sections[0]
                last_section = train_sections[-1]

                # Formatage de la durée
                duration_minutes = journey.get('duration', 0) // 60
                if duration_minutes >= 60:
                    hours = duration_minutes // 60
                    minutes = duration_minutes % 60
                    duration_str = f"{hours}h{minutes:02d}"
                else:
                    duration_str = f"{duration_minutes}min"

                formatted_journey = {
                    "name": f"Trajet {start_name} - {stop_name}",
                    "start_location": start_name,
                    "end_location": stop_name,
                    "date": journey.get('departure_date_time', '')[:10],
                    "start_hour": journey.get('departure_date_time', '')[9:11] + 'h' + journey.get(
                        'departure_date_time', '')[11:13],
                    "end_hour": journey.get('arrival_date_time', '')[9:11] + 'h' + journey.get('arrival_date_time', '')[
                                                                                   11:13],
                    "duration": duration_str,  # Format modifié
                    "train_type": first_section.get('display_informations', {}).get('commercial_mode', 'Train'),
                    "price": "Prix non disponible",
                    "description": self._build_journey_description(train_sections)
                }
                journeys.append(formatted_journey)

        return journeys

    def _build_journey_description(self, train_sections):
        """
        Construit une description détaillée du trajet
        """
        descriptions = []
        for section in train_sections:
            info = section.get('display_informations', {})
            train_name = info.get('headsign', '')
            train_type = info.get('commercial_mode', '')
            descriptions.append(f"{train_type} {train_name}")

        return " → ".join(descriptions) if descriptions else "Trajet direct"