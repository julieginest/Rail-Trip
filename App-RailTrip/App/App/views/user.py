from django.shortcuts import redirect
from django.views.generic import TemplateView
from ..models import Utilisateur

class UserView(TemplateView):
    template_name = "app_users/user.html"

    

    def get(self, request, *args, **kwargs):
        userName = request.GET.get('u',None)
        user = None
        if(userName):
            user = Utilisateur.objects.get(pseudo=userName)
            print(user.pseudo)
        else:
            redirect('login')
        context = {
                'pseudo': user.pseudo,
                'isFollowed': True,
            }
        return self.render_to_response(context)