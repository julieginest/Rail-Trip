import os
import requests
import urllib.parse as url
import json
from datetime import datetime, date
import math
from scipy.interpolate import PchipInterpolator
import numpy as np

class TransportService:
    API_KEY = "e49dbfec-a940-407b-b845-49c8fe8439b5"
    API_LINK = "https://api.sncf.com/v1/coverage/sncf"

    def _time_multiplier(self, x):
        """Calculate time-based price multiplier"""
        x_points = np.array([0, 5, 7, 10, 14, 16, 19, 24])
        y_points = np.array([0.5, 1, 2.5, 2.5, 1.5, 2.5, 2.5, 0.5])
        interpolator = PchipInterpolator(x_points, y_points)
        return interpolator(x)

    def _day_multiplier(self, x, A=2, L=0.25, k=0.1):
        """Calculate day-based price multiplier"""
        return L + (A - L) * np.exp(-k * x)

    def _network_price(self, network):
        """Get base price per kilometer for different train networks"""
        tgv = ["DB SNCF", "Eurostar", "TGV INOUI", "TGV Lyria"]
        tgv_low_cost = ["OUIGO", "OUIGO Train Classique"]
        ters = ["Aléop", "BreizhGo", "FLUO", "LEX", "MOBIGO", "NOMAD", "NightJet",
                "REGIONAURA", "RÉMI", "RÉMI Exp.", "SNCF", "SOLEA", "TER", "TER HDF", "TER NA"]
        intercite = ["Intercités", "Intercités de nuit"]

        if network in tgv:
            return 0.5
        if network in tgv_low_cost:
            return 0.25
        if network in ters:
            return 0.07
        if network in intercite:
            return 0.2
        return 0.2

    def _calculate_price(self, distance, time, network):
        """Calculate journey price based on distance, time and network"""
        try:
            if isinstance(time, str):
                time = datetime.strptime(time, "%Y%m%dT%H%M%S")
            time_float = time.hour + time.minute / 60
        except Exception as e:
            print(f"Error parsing time: {str(e)}")
            time_float = 12  # Default to noon if time parsing fails

        time_coefficient = self._time_multiplier(time_float)
        
        # Special case for Paris region transport
        if network in ["RER", "TRANSILIEN"]:
            return 2.5
            
        km_price = self._network_price(network)
        price = (time_coefficient * distance * km_price) / math.exp(distance / 1000)
        return round(price, 2)

    def find_station(self, city_name):
        """Find and return the station ID for a given city using advanced search"""
        try:
            city_name = city_name.strip().lower()
            auth_args = (self.API_KEY, '')

            # Use specific type filter for stations
            search_url = (f"{self.API_LINK}/places?"
                         f"q={url.quote(city_name)}"
                         f"&type[]=stop_area")

            print(f"Searching for {city_name} using URL: {search_url}")
            response = requests.get(search_url, auth=auth_args)

            if response.status_code != 200:
                print(f"API Error for {city_name}: {response.text}")
                raise Exception(f"Station search error: {response.text}")

            data = json.loads(response.text)
            
            if not data.get('places'):
                raise Exception(f"No station found for: {city_name}")

            # Filter results based on administrative region
            filtered_places = []
            for place in data['places']:
                if 'stop_area' in place:
                    admin_regions = place['stop_area'].get('administrative_regions', [])
                    for admin in admin_regions:
                        if city_name in admin.get('name', '').lower():
                            filtered_places.append(place)
                            break

            # Use filtered results if available, otherwise use first result
            selected_place = filtered_places[0] if filtered_places else data['places'][0]
            print(f"Selected station: {selected_place.get('name')} ({selected_place.get('id')})")
            return selected_place['id']

        except Exception as e:
            print(f"Error processing {city_name}: {str(e)}")
            raise Exception(f"Station search failed for {city_name}: {str(e)}")

    def reach(self, start, stop, journey_date=None, date_use='departure'):
        """
        Search for train journeys between two cities.
        
        Args:
            start (str): Starting city name
            stop (str): Destination city name 
            journey_date (datetime): Date and time of travel 
            date_use (str): Whether the datetime is for departure or arrival
        
        Returns:
            list: List of possible journeys with details
        """
        try:
            print(f"Searching journeys from {start} to {stop} for {journey_date}")
            
            start_id = self.find_station(start)
            stop_id = self.find_station(stop)
            
            print(f"Found stations: {start} ({start_id}) -> {stop} ({stop_id})")

            auth_args = (self.API_KEY, '')
            journey_date = journey_date or date.today()

            link = self.build_link(start_id, stop_id, journey_date, date_use)
            print(f"API Request URL: {link}")
            
            response = requests.get(link, auth=auth_args)

            if response.status_code == 200:
                data = json.loads(response.text)
                
                if not data.get("journeys"):
                    print(f"No journeys found between {start} and {stop}")
                    return []
                    
                journeys = self.sanitize_data(data)
                print(f"Found {len(journeys)} possible journeys")
                return journeys
                
            else:
                print(f"API Error Response: {response.text}")
                raise Exception(f"API Error {response.status_code}: {response.text}")

        except Exception as e:
            print(f"Error searching journeys: {str(e)}")
            raise Exception(f"Journey search failed: {str(e)}")

    def sanitize_data(self, data):
        """Process and format journey data from API response"""
        journeys = data.get("journeys", [])
        formatted_journeys = []
        
        for journey in journeys:
            total_price = 0
            steps = []
            
            for section in journey.get("sections", []):
                if section["type"] == "public_transport":
                    # Calculer le prix pour cette étape
                    step_price = self._calculate_price(
                        section["geojson"]["properties"][0]["length"] / 1000,
                        section["departure_date_time"],
                        section["display_informations"]["network"]
                    )
                    total_price += step_price

                    # Formater les dates
                    departure_dt = datetime.strptime(section["departure_date_time"], "%Y%m%dT%H%M%S")
                    arrival_dt = datetime.strptime(section["arrival_date_time"], "%Y%m%dT%H%M%S")

                    step = {
                        "type": section["type"],
                        "network": section["display_informations"]["network"],
                        "from": section["from"]["name"],
                        "to": section["to"]["name"],
                        "departure_date": departure_dt.strftime("%d/%m/%Y"),
                        "arrival_date": arrival_dt.strftime("%d/%m/%Y"),
                        "departure_time": departure_dt.strftime("%H:%M"),
                        "arrival_time": arrival_dt.strftime("%H:%M"),
                        "raw_departure": section["departure_date_time"],
                        "raw_arrival": section["arrival_date_time"],
                        "price": round(step_price, 2)
                    }
                    steps.append(step)

            if steps:
                # Ajouter le prix total au premier step
                steps[0]["total_price"] = round(total_price, 2)
                formatted_journeys.append(steps)

        return formatted_journeys

    def build_link(self, start_id, stop_id, date_obj, date_use):
        """Build the API request URL for journey search"""
        date_str = date_obj.strftime("%Y%m%dT%H%M%S")
        
        url = (f"{self.API_LINK}/journeys?"
               f"from={start_id}&"
               f"to={stop_id}&"
               f"datetime={date_str}&"
               f"datetime_represents={date_use}&"
               f"count=5&"
               f"min_nb_journeys=3&"
               f"depth=3&"
               f"disable_geojson=false&"
               f"equipment_details=false")
               
        return url
