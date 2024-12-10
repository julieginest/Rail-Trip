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
    API_OSM = 'https://nominatim.openstreetmap.org/search.php?format=jsonv2&q='

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        ]

    def reach(self, start, stop, journey_date=None, date_use='departure'):
        auth_args = (self.API_KEY, '')
        journey_date = journey_date or date.today()

        link = self.build_link(start, stop, journey_date, date_use)
        print("my link", link)
        response = requests.get(link, auth=auth_args)

        if response.status_code == 200:
            return json.loads(response.text)
        raise Exception(f"API Error: {response.status_code} - {response.text}")

    def build_link(self, start, stop, date_obj, date_use):
        start = self.osm_reach(start)
        stop = self.osm_reach(stop)
        date_str = date_obj.strftime("%Y%m%dT%H%M%S")

        return f"{self.API_LINK}/journeys?from={start}&to={stop}&datetime={date_str}&datetime_represents={date_use}"

    def osm_reach(self, search):
        time.sleep(1.5)
        try:
            parsed = list(search.split(";"))
            long = float(parsed[0].replace(",", "."))
            lat = float(parsed[1].replace(",", "."))
            return url.quote(f"{long};{lat}")
        except:
            headers = {'User-Agent': random.choice(self.user_agents)}
            response = requests.get(f"{self.API_OSM}{url.quote(search + ' France')}", headers=headers)
            data = json.loads(response.text)
            return url.quote(f"{data[0]['lon']};{data[0]['lat']}")