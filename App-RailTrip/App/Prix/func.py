from scipy.interpolate import PchipInterpolator
import numpy as np

# Définition de la fonction
def smooth_f_function(x):
    """
    Retourne la valeur de la fonction lissée f(x) pour un x donné.
    
    Paramètre:
        x (float ou np.ndarray): La valeur d'entrée dans l'intervalle [0, 24].
    
    Retourne:
        float ou np.ndarray: La valeur de f(x).
    """
    # Points d'interpolation
    x_points = np.array([0, 5,7, 10, 14, 16, 19, 24])
    y_points = np.array([0.5, 1,2.5 , 2.5, 1.5, 2.5, 2.5, 0.5])
    
    # Création de l'interpolateur
    interpolator = PchipInterpolator(x_points, y_points)
    
    # Retour de la valeur interpolée
    return interpolator(x)

# Exemple d'utilisation
x_value = 6  # Point à évaluer
result = smooth_f_function(x_value)
print(f"f({x_value}) = {result}")