from datetime import date, timedelta

import requests  # Pour les appels
import urllib.parse as url
import json
import time
import random

##### Pour .env #####
import os
from dotenv import load_dotenv

#####################

# Récupération du .env
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_LINK = os.getenv('API_LINK')

# Lien de l'API OSM
API_OSM = 'https://nominatim.openstreetmap.org/search.php?format=jsonv2&q='

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]


# Appel 'API
def Reach(start, stop, date=date.today(), dateUse='departure'):
    """
    Effectue un appel à l'API de transport pour obtenir un itinéraire.

    Args:
        start (str): Point de départ (adresse ou coordonnées "long;lat")
        stop (str): Point d'arrivée (adresse ou coordonnées "long;lat")
        date (date): Date du trajet (défaut: aujourd'hui)
        dateUse (str): Type de date ('departure' ou 'arrival')



    Returns:
        dict: Résultat de la requête en format JSON

    Raises:
        Exception: Si la requête échoue
    """
    # Tuple pour l'authentification
    authArgs = (API_KEY, '')

    # Construction du lien avec les paramètres fournis
    link = buildLink(start, stop, date, dateUse)

    # Appel à l'API
    response = requests.get(link, auth=authArgs)

    # Vérification de la réponse
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise Exception(f"Erreur API : {response.status_code} - {response.text}")


# Génération du lien
def buildLink(start, stop, date=date.today(), dateUse='departure'):
    start = OSM_Reach(start)
    stop = OSM_Reach(stop)
    date = date.strftime("%Y%m%dT%H%M%S")

    Link = API_LINK + "/journeys?from=" + start + "&to=" + stop + "&datetime=" + date + "&datetime_represents=" + dateUse

    ## Test ##
    print(Link)
    ##########

    return (Link)


def OSM_Reach(search):
    global user_agents
    time.sleep(1.5)
    try:
        parsed = list(search.split(";"))
        long = float(parsed[0].replace(",", "."))
        lat = float(parsed[1].replace(",", "."))
        return (url.quote(long + ";" + lat))

    except:
        headers = {'User-Agent': random.choice(user_agents)}
        reponse = requests.get(API_OSM + url.quote(search + " France"), headers=headers)
        reponse = reponse.text

        reponse = json.loads(reponse)

        return (url.quote(reponse[0]["lon"] + ";" + reponse[0]["lat"]))


## Test ##
def exemple_recherche_itineraire():
    """
    Fonction exemple montrant différentes utilisations de l'API de transport.
    """
    try:
        # 1. Recherche simple Paris -> Lyon pour aujourd'hui
        print("\n1. Recherche simple Paris -> Lyon")
        resultats = Reach("Paris Gare de Lyon", "Lyon Part Dieu")
        print(f"Itinéraires trouvés pour aujourd'hui !")

        # 2. Recherche avec date spécifique
        print("\n2. Recherche pour demain")
        demain = date.today() + timedelta(days=1)
        resultats = Reach(
            start="Marseille Saint Charles",
            stop="Paris Gare de Lyon",
            date=demain,
            dateUse='departure'
        )
        print(f"Itinéraires trouvés pour demain !")

        # 3. Recherche avec coordonnées
        print("\n3. Recherche avec coordonnées")
        resultats = Reach(
            start="2.3522,48.8566",  # Coordonnées de Paris
            stop="4.8357,45.7640",  # Coordonnées de Lyon
            dateUse='arrival'
        )
        print("Itinéraires trouvés avec coordonnées !")

        # 4. Traitement des résultats (exemple)
        if 'journeys' in resultats:
            for i, journey in enumerate(resultats['journeys'], 1):
                print(f"\nItinéraire {i}:")
                print(f"Durée: {journey.get('duration', 'N/A')} minutes")
                print(f"Départ: {journey.get('departure_date_time', 'N/A')}")
                print(f"Arrivée: {journey.get('arrival_date_time', 'N/A')}")

    except Exception as e:
        print(f"Erreur : {str(e)}")