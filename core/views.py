from django.shortcuts import render, get_object_or_404
# Importation correcte depuis l'application hotels
from hotels.models import Hotel

# Afficher la page d'accueil
def home(request):
    featured_hotels = Hotel.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'hotels': featured_hotels})