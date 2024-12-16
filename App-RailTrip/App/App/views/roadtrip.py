from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from ..models import RoadTrip, Utilisateur

class RoadTripCreateView(CreateView):
    model = RoadTrip
    template_name = 'app_users/roadtrip/create.html'
    fields = ['description', 'publique', 'depart', 'nbjour']
    success_url = reverse_lazy('enregistrements')
    login_url = 'login'

    def dispatch(self, request, *args, **kwargs):
        # If user_id doesn't exist in request.session then the user is not logged in
        if 'user_id' not in request.session:
            # Go to login page
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # We're getting the user id
        user_id = self.request.session.get('user_id')
        try:
            utilisateur = Utilisateur.objects.get(id=user_id)
            
            # Steps forms of the roadtrip
            etape1 = self.request.POST.get('etape1')
            etape2 = self.request.POST.get('etape2')
            
            form.instance.etapes = f"{etape1},{etape2}"
            form.instance.utilisateur = utilisateur
            
            return super().form_valid(form)
        except Utilisateur.DoesNotExist:
            # If the user doesn't exist for x reason we are redirecting him to login page
            return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
