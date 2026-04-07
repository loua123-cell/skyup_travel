from django.db import models

class Tour(models.Model):
    """Modèle principal pour les voyages organisés."""
    title = models.CharField(max_length=200, verbose_name="Titre du voyage")
    description = models.TextField(verbose_name="Description générale")
    base_price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Prix à partir de (TND)")
    duration_nights = models.IntegerField(default=7, verbose_name="Nombre de nuits")
    
    # Inclusions et Exclusions (Format texte libre ou liste)
    inclusions = models.TextField(verbose_name="Ce prix comprend")
    exclusions = models.TextField(verbose_name="Ce prix ne comprend pas")
    
    image = models.ImageField(upload_to='tours/', verbose_name="Image principale")

    class Meta:
        verbose_name = "Voyage Organisé"
        verbose_name_plural = "Voyages Organisés"

    def __str__(self):
        return self.title

class ItineraryDay(models.Model):
    """Programme détaillé jour par jour."""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField(verbose_name="Jour n°")
    title = models.CharField(max_length=200, verbose_name="Titre de la journée")
    content = models.TextField(verbose_name="Détails du programme")
    accommodation = models.CharField(max_length=255, blank=True, verbose_name="Hébergement prévu")

    class Meta:
        ordering = ['day_number']
        unique_together = ['tour', 'day_number']

class TourInclusion(models.Model):
    """Détails spécifiques des prestations (Vols inclus, Hôtels, etc.)."""
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='highlights')
    service_name = models.CharField(max_length=255) # ex: 4 Nuits à bord du bateau
    category = models.CharField(max_length=50, choices=[('HOTEL', 'Hôtel'), ('FLIGHT', 'Vol'), ('VISIT', 'Visite')])

    def __str__(self):
        return self.service_name