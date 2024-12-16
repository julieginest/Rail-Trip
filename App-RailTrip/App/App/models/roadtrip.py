from django.db import models
from .user import Utilisateur

class RoadTrip(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)  # Nouveau champ
    publique = models.BooleanField(default=False)
    etapes = models.CharField(max_length=255)
    depart = models.DateField()
    nbjour = models.IntegerField()
    description = models.CharField(max_length=255)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - RoadTrip de {self.utilisateur.pseudo}"
