from django.db import models
from .user import Utilisateur
from datetime import datetime 

class RoadTrip(models.Model):
    # Identifiant unique
    id = models.AutoField(primary_key=True)
    
    # Nom généré automatiquement ou personnalisé
    nom = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Nom du voyage"
    )
    
    # Utilisateur propriétaire
    utilisateur = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE,
        related_name='roadtrips',
        verbose_name="Voyageur"
    )
    
    # Description du voyage
    description = models.TextField(
        max_length=500, 
        verbose_name="Description du voyage"
    )
    
    # Visibilité du roadtrip
    publique = models.BooleanField(
        default=False, 
        verbose_name="Voyage public"
    )
    
    # Date de départ (obligatoire)
    depart = models.DateTimeField(
        verbose_name="Date de départ", 
        null=False,
        blank=False
    )
    
    # Date de retour (optionnelle)
    retour = models.DateTimeField(
        verbose_name="Date de retour", 
        null=True,
        blank=True
    )
    
    # Nombre de jours
    nbjour = models.PositiveIntegerField(
        verbose_name="Nombre de jours",
        default=1
    )
    
    # Étapes du voyage en JSON
    etapes = models.JSONField(
        default=list,
        verbose_name="Étapes du voyage"
    )
    
    # Prix total du voyage
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
        # Calculer le nombre de jours
        if self.depart and self.retour:
            self.nbjour = (self.retour - self.depart).days + 1
        
        # Générer un nom si non spécifié
        if not self.nom and self.depart:
            self.nom = f"Voyage {self.depart.strftime('%d/%m/%Y')}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom or 'Nouveau Voyage'} - Voyage de {self.utilisateur.pseudo}"
