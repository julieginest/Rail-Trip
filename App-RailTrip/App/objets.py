from django.db import models

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    mdp = models.CharField(max_length=128)  
    pseudo = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(unique=True)
    
    def __str__(self):
        return self.pseudo
    
class RoadTrip(models.Model):
    id = models.AutoField(primary_key=True)
    etapes = models.CharField()
    depart = models.DateField()
    nbjour = models.IntegerField()
    description = models.CharField()
    utilisateur = models.ForeignKey(Utilisateur)
