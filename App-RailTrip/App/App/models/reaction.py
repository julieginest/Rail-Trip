from django.db import models
from .roadtrip import RoadTrip
from .user import Utilisateur


class Reaction(models.Model):
    id = models.AutoField(primary_key=True)
    like = models.BooleanField(default=False)
    roadtrip = models.ForeignKey(RoadTrip, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
