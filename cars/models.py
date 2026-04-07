from django.db import models

class Car(models.Model):
    # Liste des types de transmission
    TRANSMISSION_CHOICES = [
        ('MANUAL', 'Manuelle'),
        ('AUTOMATIC', 'Automatique'),
    ]

    # Liste des types de carburant
    FUEL_CHOICES = [
        ('GASOLINE', 'Essence'),
        ('DIESEL', 'Diesel'),
        ('HYBRID', 'Hybride'),
        ('ELECTRIC', 'Électrique'),
    ]

    # Détails du véhicule
    brand = models.CharField(max_length=50) # Exemple: Renault, Kia, Fiat
    model_name = models.CharField(max_length=50) # Exemple: Clio 4, Sportage
    year = models.PositiveIntegerField() # Année de fabrication
    # Caractéristiques techniques
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='MANUAL')
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='GASOLINE')
    seats = models.PositiveIntegerField(default=5) # Nombre de places
    
    # Prix et Disponibilité
    price_per_day = models.DecimalField(max_digits=10, decimal_places=3) # Prix en TND par jour
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model_name}"

        # cars/models.py

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.car.brand} by {self.customer_name}"