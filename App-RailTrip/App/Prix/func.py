from scipy.interpolate import PchipInterpolator
import numpy as np
import datetime
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

def prix(distance, dateTime, network):
    timeFloat = dateTime.hour + dateTime.minute / 60
    coefHeure = multiplicatHeure(timeFloat)

    kmPrice = 0.3
    match network:
        case 'TGV INOUI':
            kmPrice = 0.5
        case 'OUIGO':
            kmPrice = 0.25
    
    

    return (coefHeure * kmPrice * distance)/math.exp(distance / 1000)