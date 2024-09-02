from datetime import date

import requests # Pour les appels

##### Pour .env #####
import os
from dotenv import load_dotenv
#####################

# Récupération du .env
load_dotenv("../../../.env")
API_KEY = os.getenv('API_KEY')
API_LINK = os.getenv('API_LINK')

# Lien de l'API OSM
API_OSM='https://nominatim.openstreetmap.org/search.php?format=jsonv2&'


#Appel 'API
def Reach():

    # Tuple d'authentification
    authArgs = (API_KEY,'')
    
    # Requete
    # response = requests.get(API_LINK+"/journeys?from=18%20rue%20des%20sazieres%20colombes%20france&to=gare%20montparnasse&", auth=authArgs)
    response = requests.get(API_LINK+"/places?q=18%20rue%20des%20sazieres%20colombes%20france&", auth=authArgs)

    ## Test ##
    status = response.text
    print(status)
    ##########

# Génération du lien
def buildLink(start, stop, date=date.today(), dateUse='start'):

    


    Link = API_LINK + ""
    
    return('')


def OSM_Reach(search):
    
    try:
        parsed = list(search.split(";"))
        long = float(parsed[0].replace(",","."))
        lat = float(parsed[1].replace(",","."))
        return((long,lat))

    except:
        pass
    
    



Reach()

