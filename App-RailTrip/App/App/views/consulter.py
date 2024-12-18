from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView
from ..models import Favori, RoadTrip
from ..models import Utilisateur

class ConsulterView(TemplateView):
    template_name = "app_users/consulter.html"

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

        roadtrips = RoadTrip.objects.filter(publique=1).exclude(utilisateur=user).select_related("utilisateur")

        duree_filter=self.request.GET.get('duree')
        if duree_filter:
            roadtrips = roadtrips.filter(nbjour=duree_filter)

        depart_filter = self.request.GET.get('depart') 
        if depart_filter: 
            roadtrips = roadtrips.filter( etapes__startswith=depart_filter )

        context["roadtrips"] = roadtrips
        return context
    
class AjouterFavoriView(View):
    def post(self, request, roadtrip_id):
        # Récupérer l'utilisateur connecté
        user_id = request.session.get("user_id")
        utilisateur = get_object_or_404(Utilisateur, id=user_id)

        # Récupérer le roadtrip à ajouter
        roadtrip = get_object_or_404(RoadTrip, id=roadtrip_id)

        # Vérifie si ce favori existe déjà
        if Favori.objects.filter(roadtrip=roadtrip, utilisateur=utilisateur).exists():
            messages.info(request, "Ce roadtrip est déjà dans vos favoris.")
        else:
            # Ajouter le favori
            Favori.objects.create(roadtrip=roadtrip, utilisateur=utilisateur)
            messages.success(request, "Roadtrip ajouté aux favoris avec succès!")

        return redirect("consulter")