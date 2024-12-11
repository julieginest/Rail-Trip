from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView
from ..forms import RegisterForm

class RegisterView(FormView):
    template_name = "app_users/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Bienvenue {user.pseudo} sur RailTrip")
        # Redirection vers la page du profil après succès
        return redirect("profile")  # Assurez-vous que 'profile' est le nom du chemin vers votre page profile.html

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire contient des erreurs.")
        return super().form_invalid(form)
