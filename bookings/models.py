from django.db import models
from django.conf import settings
from flights.models import Flight
from hotels.models import Room
from cars.models import Car

class Booking(models.Model):
    # Liste des statuts possibles pour une réservation
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('CONFIRMED', 'Confirmée'),
        ('CANCELLED', 'Annulée'),
    ]

    # Relation avec l'utilisateur (Le client qui effectue la réservation)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="Client"
    )
    
    # Références vers les différents services (Peuvent être nulles si le service n'est pas choisi)
    flight = models.ForeignKey(Flight, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vol")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Chambre d'hôtel")
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Voiture de location")

    # Détails de planification
    booking_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    start_date = models.DateField(verbose_name="Date de début / Check-in")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin / Check-out")

    # Informations financières et état du dossier
    total_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Prix Total (TND)")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING', 
        verbose_name="Statut du dossier"
    )

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-booking_date'] # Les réservations les plus récentes apparaissent en haut

    def __str__(self):
        # Format d'affichage dans l'interface d'administration
        return f"Réservation #{self.id} par {self.user.username} ({self.status})"