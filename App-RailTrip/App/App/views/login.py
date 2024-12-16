from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from ..forms import LoginForm

class LoginView(FormView):
    template_name = "app_users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.get_user()
        # Store user ID in session
        self.request.session["user_id"] = user.id
        messages.success(self.request, f"{pseudo}, connexion réussie.")
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")  # Added self.request
        return redirect('home')