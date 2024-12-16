from __future__ import annotations

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import models

class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    mdp = models.CharField(max_length=128)
    pseudo = models.CharField(max_length=50, unique=True)

    @classmethod
    def newUtilisateur(cls, pseudo: str, mdp: str):
        return cls.objects.create(pseudo=pseudo, mdp=make_password(mdp))

    @classmethod
    def deleteUtilisateur(cls, user: Utilisateur, mdp:str):
        if not isinstance(user, cls):
            raise ValueError("L'utilisateur fourni dans deleteUtilisateur n'est pas de type 'Utilisateur'")

        if not check_password(user.mdp, mdp):
            raise ValidationError("Le mot de passe n'est pas correct")

        user.delete()

    @property
    # Le système d'auth de base de django possède un attribut is_authenticated, pour ne pas avoir
    # de problèmes avec on le met ici
    def is_authenticated(self):
        return True

    def userFollow(self, user_to_follow):
        from .followers import Relation
        Relation.objects.get_or_create(follower=self, followed=user_to_follow)

    def unfollow(self, user_to_unfollow):
        from .followers import Relation
        Relation.objects.filter(follower=self, followed=user_to_unfollow).delete()

    def is_following(self, user):
        from .followers import Relation
        return Relation.objects.filter(follower=self, followed=user).exists()

    def get_followers(self):
        return Utilisateur.objects.filter(following__followed=self)

    def get_following(self):
        return Utilisateur.objects.filter(followers__follower=self)