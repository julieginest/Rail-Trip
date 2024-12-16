from scipy.interpolate import PchipInterpolator
import numpy as np
from datetime import datetime
import math

# Définition de la fonction
def multiplicatHeure(x):
    """
    Retourne la valeur de la fonction lissée f(x) pour un x donné.
    
    Paramètre:
        x (float ou np.ndarray): La valeur d'entrée dans l'intervalle [0, 24].
    
    Retourne:
        float ou np.ndarray: La valeur de f(x).
    """
    # Points d'interpolation
    x_points = np.array([0  , 5,  7   , 10 , 14 , 16 , 19 , 24])
    y_points = np.array([0.5, 1,  2.5 , 2.5, 1.5, 2.5, 2.5, 0.5])
    
    # Création de l'interpolateur
    interpolator = PchipInterpolator(x_points, y_points)
    
    # Retour de la valeur interpolée
    return interpolator(x)

# Exemple d'utilisation
x_value = 6  # Point à évaluer
result = multiplicatHeure(x_value)
# print(f"f({x_value}) = {result}")


def multiplicatJour(x, A=2, L=0.25, k=0.1):

    """

    Retourne la valeur de la fonction exponentielle décroissante.



    Paramètres :

    - x : valeur ou tableau de valeurs (float ou numpy.ndarray)

    - A : valeur initiale (float, par défaut 2)

    - L : limite asymptotique (float, par défaut 0.25)

    - k : taux de décroissance (float, par défaut 0.1)



    Retour :

    - f(x) : valeur de la fonction pour x (float ou numpy.ndarray)

    """

    return L + (A - L) * np.exp(-k * x)

def nwPrice(network):
    tgv = [
        "DB SNCF",
        "Eurostar",
        "TGV INOUI",
        "TGV Lyria",
    ]
    tgvLowCost = [
        "OUIGO",
        "OUIGO Train Classique",
    ]
    TERs = [
        "Aléop",
        "BreizhGo",
        "FLUO",
        "LEX",
        "MOBIGO",
        "NOMAD",
        "NightJet",
        "REGIONAURA",
        "RÉMI",
        "RÉMI Exp.",
        "SNCF",
        "SOLEA",
        "TER",
        "TER HDF",
        "TER NA",
    ]
    intercite=[
        "Intercités",
        "Intercités de nuit",
    ]

    if network in tgv:
        return 0.5
    if network in tgvLowCost:
        return 0.25
    if network in TERs:
        return 0.07
    if network in intercite:
        return 0.2
    return 0.2

def prix(distance, dateTime, network):
    timeFloat = 0
    try:
        timeFloat = dateTime.hour + dateTime.minute / 60
    except:
        dateTime = datetime.strptime(dateTime,"%Y%m%dT%H%M%S")
        timeFloat = dateTime.hour + dateTime.minute / 60
    coefHeure = multiplicatHeure(timeFloat)
    idfm = [
        "RER",
        "TRANSILIEN",
    ]
    if(network in idfm):
        roundedPrice=2.5
    else:
        kmPrice = nwPrice(network)
        
        
        price = (coefHeure * distance * kmPrice)/math.exp(distance / 1000)
        roundedPrice = round(price,2)
    print(roundedPrice)
    return roundedPrice

## TEST ##
# print(prix(250,datetime.datetime(2024,2,2,2,2), "TGV INOUI"))
## #### ##20241222T144900