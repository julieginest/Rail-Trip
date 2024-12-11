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
        user = form.get_user()
        # Store user ID in session
        self.request.session["user_id"] = user.id
        messages.success(self.request, f"Bienvenue, {user.pseudo}.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "Le pseudo ou le mot de passe est incorrect.")
        return self.render_to_response(self.get_context_data(form=form))
