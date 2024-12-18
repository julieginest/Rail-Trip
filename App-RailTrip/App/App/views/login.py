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
        # We are storing the user ID in the self.request so we can check use it as a instance once the user is connected.
        self.request.session["user_id"] = user.id
        messages.success(self.request, f"{user.pseudo}, connexion réussie.")
        return redirect('home')

    def form_invalid(self, form):
        messages.error(self.request, "Le formulaire est invalide.")  # Added self.request
        return redirect('home')
