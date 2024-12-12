from django import forms
from ..models import Utilisateur
from django.contrib.auth.hashers import check_password

class LoginForm(forms.Form):
    pseudo = forms.CharField(max_length=30, required=True, label="Nom d'utilisateur")
    mdp = forms.CharField(max_length=64, widget=forms.PasswordInput, required=True, label="Mot de passe")

    def clean(self):
        cleaned_data = super().clean()
        pseudo = cleaned_data.get("pseudo")
        mdp = cleaned_data.get("mdp")

        if not pseudo or not mdp:
            raise forms.ValidationError("Tous les champs sont obligatoires.")

        try:
            user = Utilisateur.objects.get(pseudo=pseudo)
            if not check_password(mdp, user.mdp):
                raise forms.ValidationError("Le nom d'utilisateur ou le mot de passe est incorrect.")
        except Utilisateur.DoesNotExist:
            raise forms.ValidationError("Le nom d'utilisateur ou le mot de passe est incorrect.")

        return cleaned_data

    def get_user(self):
        pseudo = self.cleaned_data.get("pseudo")
        try:
            # Recherchez l'utilisateur dans le modèle Utilisateur
            user = Utilisateur.objects.get(pseudo=pseudo)
            return user
        except Utilisateur.DoesNotExist:
            return None
