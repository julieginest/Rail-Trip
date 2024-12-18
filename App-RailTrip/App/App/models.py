from django.db import models

# class Utilisateur(models.Model):
#     id = models.AutoField(primary_key=True)
#     mdp = models.CharField(max_length=128)  
#     pseudo = models.CharField(max_length=50, unique=True)
#     mail = models.EmailField(unique=True)

#     class Meta:
#       db_table = "utilisateur"
    
    
# class RoadTrip(models.Model):
#     id = models.AutoField(primary_key=True)
#     publique = models.BooleanField(default = False)
#     titre = models.CharField()
#     etapes = models.CharField()
#     depart = models.DateField()
#     nbjour = models.IntegerField()
#     description = models.TextField()
#     utilisateur = models.ForeignKey(Utilisateur)

#     class Meta:
#       db_table = "roadtrip"
