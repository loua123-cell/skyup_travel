# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Route pour la réservation d'une chambre
    path('book/room/<int:room_id>/', views.book_room, name='book_room'),
    path('success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]