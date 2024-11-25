from django.views.generic import FormView
from django.contrib import messages
from ..forms import LoginForm

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        pseudo = form.cleaned_data["pseudo"]
        user = form.get_user()
        self.request.session["user_id"] = user.id
        messages.success(self.request, f"{pseudo}, connexion réussie.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error("Le formulaire est invalide.")
        return super().form_invalid(form)