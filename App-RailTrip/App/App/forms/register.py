from django import forms
from ..models import Utilisateur
from django.contrib.auth.hashers import make_password

class RegisterForm(forms.ModelForm):
    pseudo = forms.CharField(max_length=32, required=True)
    mdp = forms.CharField(widget=forms.PasswordInput, required=True, max_length=64)
    same_mdp = forms.CharField(widget=forms.PasswordInput, required=True, max_length=64, label="Confirmer le mot de passe")

    class Meta:
        model = Utilisateur
        fields = ['pseudo']
        error_messages = {
            'pseudo': {
                'max_length': "Le pseudo est trop long"
            },
            'mdp': {
                'max_length': "Le mot de passe est trop long"
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        pseudo = cleaned_data.get('pseudo')
        mdp = cleaned_data.get('mdp')
        same_mdp = cleaned_data.get('same_mdp')

        if not pseudo or not mdp or not same_mdp:
            raise forms.ValidationError("Vous n'avez pas rempli tous les champs.")

        if mdp != same_mdp:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        # On vérifie si l'utilisateur en question existe déjà
        if Utilisateur.objects.filter(pseudo=pseudo).exists():
            raise forms.ValidationError("Ce pseudo est déjà utilisé.")

        return cleaned_data

    def save(self, commit=True):
        pseudo = self.cleaned_data.get("pseudo")
        mdp = self.cleaned_data.get("mdp")
        user = Utilisateur.newUtilisateur(pseudo=pseudo, mdp=mdp)
        return user