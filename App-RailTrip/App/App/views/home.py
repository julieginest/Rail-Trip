from contextlib import nullcontext

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Vous avez était déconnecté avec succès.")
    return redirect("login")
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"
    login_url = "/login/"

    def send(self, request):
        if 'logout' in self.request.POST:
            logout(self.request)
        return redirect("home")

    def get(self, request):
        return render(request, self.template_name)