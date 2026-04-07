from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Hotel, Room

# Afficher la liste des hôtels avec options de recherche avancée
def hotel_list(request):
    # 1. Récupérer les paramètres
    query = request.GET.get('q', '')
    adults = request.GET.get('adults')
    children = request.GET.get('children')
    babies = request.GET.get('babies')

    # 2. QuerySet de base
    hotels = Hotel.objects.all()

    # 3. Filtrage textuel (Nom, Ville, Pays)
    if query:
        hotels = hotels.filter(
            Q(name__icontains=query) | 
            Q(city__icontains=query) | 
            Q(country__icontains=query)
        )

    # 4. Filtrage par capacité (Correction du bug UnboundLocalError)
    if adults or children or babies:
        # Conversion sécurisée en entiers
        nb_adults = int(adults) if adults and adults.isdigit() else 0
        nb_children = int(children) if children and children.isdigit() else 0
        nb_babies = int(babies) if babies and babies.isdigit() else 0

        # Filtrer directement les hôtels via la relation inverse 'rooms'
        # C'est plus propre et évite de créer des variables intermédiaires fragiles
        hotels = hotels.filter(
            rooms__max_adults__gte=nb_adults,
            rooms__max_children__gte=nb_children,
            rooms__max_babies__gte=nb_babies,
            rooms__is_available=True
        ).distinct()

    # 5. Retourner le template
    return render(request, 'hotels/hotel_list.html', {
        'hotels': hotels, 
        'query': query,
        'adults': adults,
        'children': children,
        'babies': babies
    })

# Afficher les détails d'un hôtel spécifique
def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    
    # Récupérer les filtres pour affiner l'affichage des chambres
    adults = request.GET.get('adults', 0)
    children = request.GET.get('children', 0)
    
    rooms = hotel.rooms.filter(is_available=True)
    
    # Filtrer les chambres dans la page de détails si nécessaire
    if adults and str(adults).isdigit():
        rooms = rooms.filter(max_adults__gte=int(adults))
    if children and str(children).isdigit():
        rooms = rooms.filter(max_children__gte=int(children))
    
    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'rooms': rooms
    })