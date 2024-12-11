from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from ..forms import LoginForm

class LoginView(FormView):
    template_name = "app_users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        pseudo = form.cleaned_data["pseudo"]
        user = form.get_user()
        self.request.session["user_id"] = user.id
        messages.success(self.request, f"{pseudo}, connexion réussie.")
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")  # Added self.request
        return redirect('login')