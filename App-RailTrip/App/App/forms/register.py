from django import forms
from ..models import Utilisateur
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    pseudo = forms.CharField(max_length=32, required=True, label="Nom d'utilisateur")
    mdp = forms.CharField(widget=forms.PasswordInput, required=True, max_length=64, label="Mot de passe")
    same_mdp = forms.CharField(widget=forms.PasswordInput, required=True, max_length=64, label="Confirmer le mot de passe")
    accept_terms = forms.BooleanField(required=True, label="J'accepte les conditions générales d'utilisation")

    class Meta:
        model = Utilisateur
        fields = ['pseudo']
        error_messages = {
            'pseudo': {
                'max_length': "Le pseudo est trop long",
            },
            'mdp': {
                'max_length': "Le mot de passe est trop long",
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        pseudo = cleaned_data.get('pseudo')
        mdp = cleaned_data.get('mdp')
        same_mdp = cleaned_data.get('same_mdp')

        # Validation de base
        if not pseudo or not mdp or not same_mdp:
            raise forms.ValidationError("Tous les champs sont obligatoires.")

        if mdp != same_mdp:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        # Vérification du pseudo
        if Utilisateur.objects.filter(pseudo=pseudo).exists():
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")

        return cleaned_data

    def save(self, commit=True):
        pseudo = self.cleaned_data["pseudo"]
        mdp = make_password(self.cleaned_data["mdp"])  # Hashage du mot de passe
        user = Utilisateur(pseudo=pseudo, mdp=mdp)
        if commit:
            user.save()
        return user
