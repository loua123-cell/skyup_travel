from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Car, Booking
from .forms import BookingForm
from django.utils.translation import gettext as _

def car_list(request):
    """
    Récupère la liste des véhicules avec un filtrage par catégorie de prix.
    """
    category = request.GET.get('category')
    search_query = request.GET.get('q')
    cars = Car.objects.filter(is_available=True)

    if search_query:
        # Filtrer par nom ou ville
        cars = cars.filter(
            Q(name__icontains=search_query) | 
            Q(city__icontains=search_query)
        )

    if category == 'petit':
        cars = cars.filter(price_per_day__lt=150)
    elif category == 'moyen':
        cars = cars.filter(price_per_day__gte=150, price_per_day__lte=400)
    elif category == 'luxe':
        cars = cars.filter(price_per_day__gt=400)
    
    return render(request, 'cars/car_list.html', {'cars': cars, 'category': category, 'search_query': search_query})

def car_detail(request, pk):
    """
    Affiche les détails d'un véhicule et traite la réservation via BookingForm.
    """
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.save()
            
            success_msg = _("Votre réservation pour la %(brand)s a été enregistrée avec succès !") % {'brand': car.brand}
            messages.success(request, success_msg)
            
            return redirect('car_detail', pk=pk)
    else:
        form = BookingForm()
        
    return render(request, 'cars/car_detail.html', {
        'car': car, 
        'form': form,
    })

@login_required
def dashboard(request):
    """
    Affiche la liste de toutes les réservations pour l'administrateur.
    """
    # Vérification si l'utilisateur est un membre du staff
    if not request.user.is_staff:
        return redirect('car_list')
        
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'cars/dashboard.html', {'bookings': bookings})

@login_required
def delete_booking(request, pk):
    """
    Supprime une réservation spécifique.
    """
    if request.user.is_staff:
        booking = get_object_or_404(Booking, pk=pk)
        booking.delete()
        messages.warning(request, _("La réservation a été supprimée."))
    
        return redirect('cars:car_detail', pk=pk)