from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from App.models import Utilisateur


@login_required
@require_POST
def follow(request, utilisateur_id):
    # Get l'utilisateur à suivre
    utilisateur_to_follow = get_object_or_404(Utilisateur, id=utilisateur_id)

    current_utilisateur = get_object_or_404(Utilisateur, pseudo=request.user.username)

    if current_utilisateur.id != utilisateur_to_follow.id:
        try:
            current_utilisateur.userFollow(utilisateur_to_follow)
            messages.success(request, f"Vous suivez maintenant {utilisateur_to_follow.pseudo}")
        except Exception as e:
            messages.error(request, f"Impossible de suivre {utilisateur_to_follow.pseudo}. {str(e)}")
    else:
        messages.warning(request, "Vous ne pouvez pas vous suivre vous-même")

    return HttpResponseRedirect(reverse('profil', kwargs={'utilisateur_id': utilisateur_id}))


@login_required
@require_POST
def unfollow(request, utilisateur_id):
    utilisateur_to_unfollow = get_object_or_404(Utilisateur, id=utilisateur_id)

    current_utilisateur = get_object_or_404(Utilisateur, pseudo=request.user.username)

    try:
        current_utilisateur.unfollow(utilisateur_to_unfollow)
        messages.success(request, f"Vous ne suivez plus {utilisateur_to_unfollow.pseudo}")
    except Exception as e:
        messages.error(request, f"Impossible d'arrêter de suivre {utilisateur_to_unfollow.pseudo}. {str(e)}")

    return HttpResponseRedirect(reverse('profil', kwargs={'utilisateur_id': utilisateur_id}))