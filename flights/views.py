from django.shortcuts import render
from .models import Flight, Airport
from django.db.models import Q

def flight_search(request):
    """Gère la recherche de vols avec filtres avancés (Budget, Escale, Ville)."""
    
    # Récupération de tous les vols par défaut
    vols = Flight.objects.all()
    
    # 1. Filtre par Ville de Départ et d'Arrivée
    depart = request.GET.get('dep')
    arrivee = request.GET.get('arr')
    
    if depart:
        vols = vols.filter(departure_airport__city__icontains=depart)
    if arrivee:
        vols = vols.filter(arrival_airport__city__icontains=arrivee)

    # 2. Filtre par Budget (Min et Max)
    min_price = request.GET.get('min_p')
    max_price = request.GET.get('max_p')
    if min_price:
        vols = vols.filter(price__gte=min_price)
    if max_price:
        vols = vols.filter(price__lte=max_price)

    # 3. Filtre par Type de Vol (Direct vs Escale)
    vol_type = request.GET.get('type')
    if vol_type == 'direct':
        vols = vols.filter(is_direct=True)
    elif vol_type == 'escale':
        vols = vols.filter(is_direct=False)

    # Contexte pour le template
    context = {
        'vols': vols,
        'count': vols.count(),
        # Renvoi des valeurs saisies pour garder le formulaire rempli
        'query_params': request.GET 
    }
    
    return render(request, 'flights/flight_list.html', context)