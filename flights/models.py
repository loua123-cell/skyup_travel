from django.db import models

class Airport(models.Model):
    """Représente un aéroport (ex: Tunis Carthage, Paris Orly)."""
    name = models.CharField(max_length=100, verbose_name="Nom de l'aéroport")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code IATA") # ex: TUN, ORY
    city = models.CharField(max_length=100, verbose_name="Ville")

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    """Détails d'un vol spécifique avec gestion des escales et tarifs."""
    airline = models.CharField(max_length=100, verbose_name="Compagnie aérienne")
    flight_number = models.CharField(max_length=20, verbose_name="Numéro de vol")
    
    # Itinéraire
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departures')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrivals')
    
    departure_time = models.DateTimeField(verbose_name="Heure de départ")
    arrival_time = models.DateTimeField(verbose_name="Heure d'arrivée")
    
    # Filtres et options de vol
    is_direct = models.BooleanField(default=True, verbose_name="Vol Direct")
    stops_count = models.IntegerField(default=0, verbose_name="Nombre d'escales")
    
    # Prix en TND (3 décimales pour les millimes)
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Prix (TND)")
    seats_remaining = models.IntegerField(default=0, verbose_name="Sièges restants")
    is_refundable = models.BooleanField(default=False, verbose_name="Remboursable")

    class Meta:
        verbose_name = "Vol"
        ordering = ['price']

    def __str__(self):
        return f"{self.airline} : {self.departure_airport} -> {self.arrival_airport}"