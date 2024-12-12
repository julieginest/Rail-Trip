from django.shortcuts import render, redirect
from django.views import View
from ..models import Utilisateur

class ProfileView(View):
    template_name = "app_users/profile.html"

    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            # Redirige vers la page de connexion si l'utilisateur n'est pas connecté
            return redirect("login")

        try:
            user = Utilisateur.objects.get(id=user_id)
        except Utilisateur.DoesNotExist:
            # Si l'utilisateur n'existe pas dans la BDD, déconnecte et redirige
            request.session.flush()
            return redirect("login")

        # Rendre la page de profil avec le pseudo de l'utilisateur
        return render(request, self.template_name, {"pseudo": user.pseudo})
