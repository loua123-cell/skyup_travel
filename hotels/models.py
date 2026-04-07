from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Hotel(models.Model):
    """Représente un hôtel et ses caractéristiques principales."""
    
    name = models.CharField(max_length=200, verbose_name="Nom de l'hôtel")
    city = models.CharField(max_length=100, verbose_name="Ville")
    country = models.CharField(max_length=100, default="Tunisie", verbose_name="Pays")
    address = models.TextField(verbose_name="Adresse exacte")
    
    # Utilisation de decimal_places=3 pour la monnaie tunisienne (Millimes)
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=3, 
        verbose_name="Prix par nuit (TND)"
    )
    description = models.TextField(blank=True, verbose_name="Description détaillée")
    
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        verbose_name="Nombre d'étoiles"
    )
    
    image = models.ImageField(
        upload_to='hotels/', 
        null=True, 
        blank=True, 
        verbose_name="Image de couverture"
    )
    
    has_wifi = models.BooleanField(default=True, verbose_name="Accès WiFi")
    has_pool = models.BooleanField(default=True, verbose_name="Piscine")
    has_parking = models.BooleanField(default=True, verbose_name="Parking gratuit")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        verbose_name = "Hôtel"
        verbose_name_plural = "Hôtels"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city} ({self.stars}★)"

class Room(models.Model):
    """Définit les types de chambres disponibles pour chaque hôtel."""
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    
    ROOM_TYPES = [
        ('SINGLE', 'Single Room'),
        ('DOUBLE', 'Double Room'),
        ('SUITE', 'Suite'),
        ('COUPLE', 'Couple Room'),
    ]
    
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='DOUBLE')
    max_adults = models.IntegerField(default=2) 
    max_children = models.IntegerField(default=1)
    max_babies = models.IntegerField(default=1)

    # Cohérence avec les décimales (3 pour le TND)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=3) 
    price_per_child = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_room_type_display()} - {self.hotel.name}"

    @property
    def total_capacity(self):
        return self.max_adults + self.max_children

class RoomImage(models.Model):
    """Galerie d'images pour une chambre spécifique."""
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.room.get_room_type_display()} - {self.room.hotel.name}"

    class Meta:
        verbose_name = "Image de Chambre"
        verbose_name_plural = "Images de Chambres"
        
class SeasonalPrice(models.Model):
    """Gère les variations de prix selon les périodes (Haute saison, etc.)."""
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seasonal_prices')
    name = models.CharField(max_length=100, verbose_name="Nom de la saison") 
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.name} : {self.room.hotel.name} ({self.price_per_night} TND)"

    class Meta:
        verbose_name = "Prix Saisonnier"
        verbose_name_plural = "Prix Saisonniers"