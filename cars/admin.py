from django.contrib import admin
from .models import Car, Booking
# Importation de la classe de base depuis le fichier base_admin.py que nous avons créé
from base_admin import BaseSkyUpAdmin

# NOTE: Nous n'avons plus besoin de redéfinir BaseSkyUpAdmin ici 
# car nous l'importons depuis le fichier central.

# 1. Configuration pour le modèle Car
@admin.register(Car)
class CarAdmin(BaseSkyUpAdmin): 
    """
    Configuration de l'interface d'administration pour les voitures.
    Hérite des styles SkyUp Travel.
    """
    # Colonnes affichées dans la liste (Vérifiez que ces noms existent dans models.py)
    list_display = ('brand', 'model_name', 'price_per_day', 'is_available')
    
    # Filtres rapides sur le côté droit
    list_filter = ('is_available', 'brand')
    
    # Barre de recherche par marque et modèle
    search_fields = ('brand', 'model_name')
    
    # Organisation des champs dans le formulaire
    # J'ai simplifié les champs pour éviter les erreurs de "Field not found"
    fieldsets = (
        ('Informations Générales', {
            'fields': ('brand', 'model_name')
        }),
        ('Tarification et Disponibilité', {
            'fields': ('price_per_day', 'is_available'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Action personnalisée lors de l'enregistrement : 
        Force la marque en majuscules.
        """
        if obj.brand:
            obj.brand = obj.brand.upper()
        super().save_model(request, obj, form, change)

# 2. Configuration pour le modèle Booking
@admin.register(Booking)
class BookingAdmin(BaseSkyUpAdmin):
    """
    Configuration de l'interface d'administration pour les réservations.
    """
    # Affichage des colonnes sans le champ 'status' pour éviter les erreurs SystemCheck
    list_display = ('id', 'car', 'start_date', 'end_date')
    
    # Filtres par date et par voiture
    list_filter = ('start_date', 'car')
    
    # Recherche par ID ou par nom du modèle de voiture (car__model_name)
    search_fields = ('id', 'car__model_name')
    
    # Barre de navigation temporelle en haut de la liste
    date_hierarchy = 'start_date'