# views.py
from django.views.generic import TemplateView

class MentionsLegalesView(TemplateView):
    template_name = "includes/mentionlegal.html"
