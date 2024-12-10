# forms.py
from django import forms

class TrajetForm(forms.Form):
    ville_depart = forms.CharField(max_length=100, required=False, label="Ville de départ")
    ville_arrivee = forms.CharField(max_length=100, required=False, label="Ville d'arrivée")
    jour_depart = forms.DateField(required=False, label="Date de départ", widget=forms.SelectDateWidget())
