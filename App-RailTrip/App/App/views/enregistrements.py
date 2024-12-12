from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views import View
from django.contrib import messages
from django.views.generic import TemplateView
from ..models import RoadTrip
from ..models import Utilisateur

class EnregistrementsView(TemplateView):
    template_name = "app_users/enregistrements.html"

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

        roadtrips = RoadTrip.objects.filter(utilisateur=user)

        context["roadtrips"] = roadtrips
        return context

class DeleteRoadTripView(View):
    def post(self, request, roadtrip_id):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")

        user = get_object_or_404(Utilisateur, id=user_id)

        roadtrip = get_object_or_404(RoadTrip, id=roadtrip_id, utilisateur=user)

        # Supprime le roadtrip
        roadtrip.delete()

        # Ajoute un message de succès
        messages.success(request, "Le roadtrip a été supprimé avec succès.")

        # Redirige vers la page des enregistrements
        return redirect("enregistrements")