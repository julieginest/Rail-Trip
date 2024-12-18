from django.db import models
from .user import Utilisateur
from datetime import datetime 

class RoadTrip(models.Model):
    id = models.AutoField(primary_key=True)
    
    nom = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Nom du voyage"
    )
    
    utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE,
        related_name='roadtrips',
        verbose_name="Voyageur"
    )
    
    description = models.TextField(
        max_length=500, 
        verbose_name="Description du voyage"
    )
    
    publique = models.BooleanField(
        default=False, 
        verbose_name="Voyage public"
    )
    
    depart = models.DateTimeField(
        verbose_name="Date de départ", 
        null=False,
        blank=False
    )
    
    retour = models.DateTimeField(
        verbose_name="Date de retour", 
        null=True,
        blank=True
    )
    
    nbjour = models.PositiveIntegerField(
        verbose_name="Nombre de jours",
        default=1
    )
    
    etapes = models.JSONField(
        default=list,
        verbose_name="Étapes du voyage"
    )
    
    prix_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        verbose_name="Prix total"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Road Trip"
        verbose_name_plural = "Road Trips"

    def save(self, *args, **kwargs):
        if self.depart and self.retour:
            self.nbjour = (self.retour - self.depart).days + 1
        
        if not self.nom and self.depart:
            self.nom = f"Voyage {self.depart.strftime('%d/%m/%Y')}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom or 'Nouveau Voyage'} - Voyage de {self.utilisateur.pseudo}"


from django.db import models
from .user import Utilisateur
from datetime import datetime


class RoadTrip(models.Model):
    id = models.AutoField(primary_key=True)

    nom = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nom du voyage"
    )

    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='roadtrips',
        verbose_name="Voyageur"
    )

    description = models.TextField(
        max_length=500,
        verbose_name="Description du voyage"
    )

    publique = models.BooleanField(
        default=False,
        verbose_name="Voyage public"
    )

    depart = models.DateTimeField(
        verbose_name="Date de départ",
        null=False,
        blank=False
    )

    retour = models.DateTimeField(
        verbose_name="Date de retour",
        null=True,
        blank=True
    )

    nbjour = models.PositiveIntegerField(
        verbose_name="Nombre de jours",
        default=1
    )

    etapes = models.JSONField(
        default=list,
        verbose_name="Étapes du voyage"
    )

    prix_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Prix total"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Road Trip"
        verbose_name_plural = "Road Trips"

    def save(self, *args, **kwargs):
        if self.depart and self.retour:
            self.nbjour = (self.retour - self.depart).days + 1

        if not self.nom and self.depart:
            self.nom = f"Voyage {self.depart.strftime('%d/%m/%Y')}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom or 'Nouveau Voyage'} - Voyage de {self.utilisateur.pseudo}"
