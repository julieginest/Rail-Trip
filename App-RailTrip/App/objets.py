from django.db import models

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    mdp = models.CharField(max_length=128)  
    pseudo = models.CharField(max_length=50, unique=True)
    mail = models.EmailField(unique=True)
    
    
class RoadTrip(models.Model):
    id = models.AutoField(primary_key=True)
    publique = models.BooleanField(default = False)
    etapes = models.CharField()
    depart = models.DateField()
    nbjour = models.IntegerField()
    description = models.CharField()
    utilisateur = models.ForeignKey(Utilisateur)

class Favori(models.Model):
    id = models.AutoField(primary_key=True)
    roadtrip = models.ForeignKey(RoadTrip)
    utilisateur = models.ForeignKey(Utilisateur)

class Reaction(models.Model):
    id = models.AutoField(primary_key=True)
    like = models.BooleanField(default = False)
    roadtrip = models.ForeignKey(RoadTrip)
    utilisateur = models.ForeignKey(Utilisateur)

