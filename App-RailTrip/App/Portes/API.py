from datetime import date

import requests # Pour les appels
import urllib.parse as url
import json
import time
import random

##### Pour .env #####
import os
from dotenv import load_dotenv
#####################

## Test ##
from sanitize import sanitizeData
## #### ##

# Récupération du .env
load_dotenv("../../../.env")
API_KEY = os.getenv('API_KEY')
API_LINK = os.getenv('API_LINK')

# Lien de l'API OSM
API_OSM='https://nominatim.openstreetmap.org/search.php?format=jsonv2&q='

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]




#Appel 'API
def Reach(Departure, Arival, date=date.today(),dateUse='departure'):

    # Tuple d'authentification
    authArgs = (API_KEY,'')
    
    # Requete
    response = requests.get(buildLink(Departure,Arival, date, dateUse), auth=authArgs)

    status = response.text
    ## Test ##
    # print("SNCF request")
    # print(status)
    # print("END SNCF REQUEST")
    ##########

    return json.loads(status)

# Génération du lien
def buildLink(start, stop, date=date.today(), dateUse='departure'):
    start = OSM_Reach(start)
    stop = OSM_Reach(stop)
    date = date.strftime("%Y%m%dT%H%M%S")


    Link = API_LINK + "/coverage/sncf/journeys?from=" + start + "&to=" + stop + "&datetime=" + date + "&datetime_represents=" + dateUse
    
    ## Test ##
    print(Link)
    ##########
    
    return(Link)


def OSM_Reach(search):
    global user_agents
    time.sleep(1.5)
    try:
        parsed = list(search.split(";"))
        long = float(parsed[0].replace(",","."))
        lat = float(parsed[1].replace(",","."))
        return(url.quote(long+";"+lat))

    except:
        headers = {'User-Agent': random.choice(user_agents)}
        reponse = requests.get(API_OSM+url.quote(search + " gare France"), headers=headers)
        reponse=reponse.text
        

        reponse = json.loads(reponse)


        return(url.quote(reponse[0]["lon"]+";"+reponse[0]["lat"]))
    


## Test ##
#print(sanitizeData(Reach("Lille", "Paris")))
