from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from hotels.models import Room
from .models import Booking  
from .forms import HotelBookingForm
from datetime import date, timedelta
from django.contrib import messages

def calculate_total_stay_price(room, start_date, end_date):
    """
    Calcule le prix total du séjour en tenant compte des tarifs saisonniers 
    pour chaque nuit entre start_date et end_date.
    """
    total_price = 0
    current_date = start_date
    
    # Boucle sur chaque nuit du séjour
    while current_date < end_date:
        # Chercher s'il existe un prix saisonnier pour cette date précise
        season = room.seasonal_prices.filter(
            start_date__lte=current_date,
            end_date__gte=current_date
        ).first()
        
        if season:
            total_price += season.price_per_night
        else:
            # Utiliser le prix de base si aucune saison n'est définie
            total_price += room.price_per_night
            
        # Passer à la nuit suivante
        current_date += timedelta(days=1)
        
    return total_price

@login_required 
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    
    if request.method == 'POST':
        form = HotelBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            
            # Calcul du nombre de nuits
            delta = booking.end_date - booking.start_date
            nights = delta.days
            
            if nights > 0:
                # UTILISATION DE LA LOGIQUE DYNAMIQUE ICI
                # On appelle la fonction de calcul au lieu d'une simple multiplication
                booking.total_price = calculate_total_stay_price(room, booking.start_date, booking.end_date)
                
                booking.status = 'PENDING'
                booking.save()
                return redirect('booking_success') 
            else:
                messages.error(request, "La date de départ doit être après la date d'arrivée.")
    else:
        form = HotelBookingForm()

    return render(request, 'bookings/book_hotel.html', {
        'form': form,
        'room': room
    })
   
@login_required
def booking_success(request):
    last_booking = Booking.objects.filter(user=request.user).order_by('-booking_date').first()
    return render(request, 'bookings/booking_success.html', {'booking': last_booking})

@login_required
def my_bookings(request):
    reservations = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'bookings/my_bookings.html', {'reservations': reservations})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    lang = getattr(request, 'LANGUAGE_CODE', 'fr')

    if booking.status == 'PENDING':
        booking.status = 'CANCELLED'
        booking.save()
        if lang == 'ar':
            messages.success(request, "تم إلغاء الحجز بنجاح.")
        else:
            messages.success(request, "La réservation a été annulée avec succès.")
    else:
        if lang == 'ar':
            messages.error(request, "لا يمكن إلغاء هذا الحجز لأنه مؤكد بالفعل.")
        else:
            messages.error(request, "Impossible d'annuler une réservation déjà confirmée.")

    return redirect('my_bookings')