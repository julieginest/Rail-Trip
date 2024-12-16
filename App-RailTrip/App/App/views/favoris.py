from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView
from ..models import Favori, RoadTrip
from ..models import Utilisateur

class FavorisView(TemplateView):
    template_name = "app_users/favoris.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.session.get("user_id")

        if user_id is None:
            return redirect("login")

        try:
            user = Utilisateur.objects.get(id=user_id)
            context["user"] = user
        except Utilisateur.DoesNotExist:
            return redirect("login")

        favoris = Favori.objects.filter(utilisateur=user)
        roadtrips = RoadTrip.objects.filter(id__in=favoris.values_list('roadtrip_id', flat=True))

        context = {
        'roadtrips': roadtrips,
    }
        return context
    
class SupprimerFavoriView(View):
    def post(self, request, roadtrip_id):
        user_id = request.session.get("user_id")

        if user_id is None:
            return redirect("login")

        # Vérifier si le favori existe pour cet utilisateur et ce roadtrip
        try:
            favori = Favori.objects.get(utilisateur_id=user_id, roadtrip_id=roadtrip_id)
            favori.delete()  # Supprimer le favori
            messages.success(request, "Favori supprimé avec succès.")
        except Favori.DoesNotExist:
            messages.error(request, "Ce favori n'existe pas.")

        return redirect("favoris")  # Rediriger vers la liste des favoris