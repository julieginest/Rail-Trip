from django.views.generic import FormView
from django.contrib import messages
from ..forms import RegisterForm

class RegisterView(FormView):
    template_name = "app_users/register.html"
    form_class = RegisterForm
    success_url = "/login/"

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, f"Bienvenue {user.pseudo} sur RailTrip")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")

        return super().form_invalid(form)