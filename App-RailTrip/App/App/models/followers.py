from django.db import models


class Relation(models.Model):
    """
    Modèle représentant une relation de suivi entre deux utilisateurs (système follower/following).

    Le modèle permet de gérer les relations de type "follow" entre les utilisateurs.

    Attributes:
        follower (ForeignKey): L'utilisateur qui suit (celui qui fait l'action de follow)
        followed (ForeignKey): L'utilisateur qui est suivi
        created_at (DateTimeField): La date et l'heure de création de la relation
    """

    follower = models.ForeignKey(
        'App.Utilisateur',
        on_delete=models.CASCADE,
        related_name='following'
    )

    followed = models.ForeignKey(
        'App.Utilisateur',
        on_delete=models.CASCADE,
        related_name='followers'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,  # Remplit automatiquement avec la date/heure à la création
    )

    class Meta:
        """
        Meta-options pour le modèle Relation.

        unique_together assure qu'un utilisateur ne peut pas
        suivre le même utilisateur plusieurs fois. Elle crée une contrainte
        dans la base de données sur les champs follower
        et followed.
        """
        unique_together = ('follower', 'followed')

    def __str__(self):
        """
        Texte de la relation.

        Return:
            str: Une string pour voir la relation, par exemple "user1 suit user2"
        """
        return f'{self.follower} suit {self.followed}'