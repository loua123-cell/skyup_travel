from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from datetime import datetime, timedelta
from .models import Hotel, Room, HotelBooking
from .forms import HotelBookingForm

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

def book_room(request, room_id):
    """
    Affiche le formulaire de réservation pour une chambre spécifique.
    """
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == 'POST':
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            
            # Calculer le prix total
            check_in = booking.check_in_date
            check_out = booking.check_out_date
            nights = (check_out - check_in).days
            
            if nights <= 0:
                messages.error(request, _("La date de départ doit être après la date d'arrivée."))
                return render(request, 'hotels/book_room.html', {'room': room, 'form': form})
            
            # Calcul du prix: prix de chambre + prix enfants
            total_price = (room.price_per_night * nights) + (room.price_per_child * booking.number_of_children * nights)
            booking.total_price = total_price
            booking.save()
            
            success_msg = _("Votre réservation pour %(room_type)s a été enregistrée avec succès !") % {
                'room_type': room.get_room_type_display()
            }
            messages.success(request, success_msg)
            
            return redirect('hotels:booking_success', booking_id=booking.id)
    else:
        form = HotelBookingForm()
    
    return render(request, 'hotels/book_room.html', {
        'room': room,
        'hotel': room.hotel,
        'form': form
    })

def booking_success(request, booking_id):
    """
    Affiche la page de confirmation de réservation.
    """
    booking = get_object_or_404(HotelBooking, pk=booking_id)
    
    # Calculer le nombre de nuits
    nights = (booking.check_out_date - booking.check_in_date).days
    
    return render(request, 'booking_success.html', {
        'booking': booking,
        'nights': nights,
        'hotel': booking.room.hotel
    })