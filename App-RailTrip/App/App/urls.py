"""
URL configuration for App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    HomeView, 
    LoginView, 
    RegisterView, 
    ProfileView, 
    logout_view, 
    EnregistrementsView, 
    DeleteRoadTripView, 
    FavorisView, 
    SupprimerFavoriView, 
    ConsulterView, 
    AjouterFavoriView, 
    follow, 
    unfollow,
    RoadTripCreateView,
    MentionsLegalesView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('logout/', logout_view , name='logout'),
    path('enregistrements/', EnregistrementsView.as_view(), name='enregistrements'),
    path('roadtrip/create/', RoadTripCreateView.as_view(), name='roadtrip'),
    path('roadtrip/delete/<int:roadtrip_id>/', DeleteRoadTripView.as_view(), name='delete_roadtrip'),
    path('favoris/', FavorisView.as_view(), name='favoris'),
    path('favoris/supprimer/<int:roadtrip_id>/', SupprimerFavoriView.as_view(), name='supprimer_favori'),
    path('consulter/', ConsulterView.as_view(), name='consulter'),
    path('ajouter_favoris/<int:roadtrip_id>/', AjouterFavoriView.as_view(), name='ajouter_favoris'),
    path('follow/<int:utilisateur_id>/', follow, name='follow'),
    path('unfollow/<int:utilisateur_id>/', unfollow, name='unfollow'),
    path('mentionlegal/', MentionsLegalesView.as_view(), name='mentionlegal')
]


