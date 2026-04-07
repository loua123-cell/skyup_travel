from django.urls import path
from . import views

urlpatterns = [
    # Route pour la recherche de vols
    path('search/', views.flight_search, name='flight_search'),
]