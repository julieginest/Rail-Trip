from django.http import HttpResponse
from django.views import View

class FavorisView(View):
    def get(self, request):
        return HttpResponse("Bonjour")