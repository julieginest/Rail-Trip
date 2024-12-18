from django.db import models
from .user import Utilisateur
from .roadtrip import RoadTrip

class Favori(models.Model):
    id = models.AutoField(primary_key=True)
    roadtrip = models.ForeignKey(RoadTrip, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
