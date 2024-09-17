from django.db import models
from .user import Utilisateur

class RoadTrip(models.Model):
    id = models.AutoField(primary_key=True)
    publique = models.BooleanField(default=False)
    etapes = models.CharField(max_length=255)  # TODO changer
    depart = models.DateField()
    nbjour = models.IntegerField()
    description = models.CharField(max_length=255) #TODO changer
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)