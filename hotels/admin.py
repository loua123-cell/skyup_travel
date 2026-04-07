# hotels/admin.py
from django.contrib import admin
from .models import Hotel, Room, SeasonalPrice, RoomImage

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    # Affichage des colonnes dans la liste des hôtels
    list_display = ('name', 'city', 'address', 'price_per_night', 'stars')
    # Filtres latéraux pour une recherche rapide
    list_filter = ('city', 'country', 'stars')
    # Barre de recherche par nom et ville
    search_fields = ('name', 'city')

# Gestion des images des chambres directement dans la page Room
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 2  # Nombre d'emplacements vides pour ajouter des photos

# Gestion des prix saisonniers directement dans la page Room
class SeasonalPriceInline(admin.TabularInline):
    model = SeasonalPrice
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # Affichage des détails techniques des chambres
    list_display = (
        'hotel', 
        'room_type', 
        'price_per_night', 
        'max_adults', 
        'max_children', 
        'max_babies', 
        'is_available'
    )
    # Filtres pour la disponibilité et les types de chambres
    list_filter = ('room_type', 'is_available', 'hotel')
    
    # Intégration des prix saisonniers et des images dans la même interface
    inlines = [SeasonalPriceInline, RoomImageInline]