from Prix.func import prix
## Test ##
# import json
# with open("dataTEST.json",'r') as file:
#     journeys = json.load(file)["journeys"]

    # print(journeys[0])
## #### ##

## DOCUMENTATION ##
"""
1) sanitizeData
    'datas' correspond au retour de l'API
    La fonction retourne une liste de possibilités de trajet composé d'une liste d'étape (c'est donc une liste dans une liste)
"""
## ############# ##


def sanitizeData(datas):
    journeys = datas["journeys"]
    formatedJourneys = []
    for journey in journeys:
        steps = []
        for p in journey["sections"]:
            if (p["type"] == "public_transport"):

                steps.append({
                    "type": p["type"], # public_transport, walking, waiting
                    "length" : p["geojson"]["properties"][0]["length"], # Longueur en metre
                    "network": p["display_informations"]["network"], # Nom du reseau (RER, Transilien, TGV INOUI, OUIGO)
                    "from": p["from"]["name"], # Lieu de départ
                    "to": p["to"]["name"], # Lieu d'arrivée

                    "departure_date_time": p["departure_date_time"], # heure de départ
                    "arrival_date_time": p["arrival_date_time"], # heure d'arrivée
                    "price": prix(p["geojson"]["properties"][0]["length"] / 1000, p["departure_date_time"], p["display_informations"]["network"])
                })
        formatedJourneys.append(steps)
    return formatedJourneys

    # print(json.dumps(formatedJourneys, indent=2))
        