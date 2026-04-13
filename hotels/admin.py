# hotels/admin.py
from django.contrib import admin
from .models import Hotel, Room, SeasonalPrice, RoomImage, HotelBooking

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

@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'room', 'check_in_date', 'check_out_date', 'total_price', 'status')
    list_filter = ('status', 'created_at', 'room__hotel')
    search_fields = ('guest_name', 'guest_email', 'guest_phone')
    readonly_fields = ('created_at', 'total_price')
    
    fieldsets = (
        ('Informations Clients', {
            'fields': ('guest_name', 'guest_email', 'guest_phone')
        }),
        ('Réservation', {
            'fields': ('room', 'check_in_date', 'check_out_date')
        }),
        ('Occupants', {
            'fields': ('number_of_adults', 'number_of_children', 'number_of_babies')
        }),
        ('Paiement et Statut', {
            'fields': ('total_price', 'status')
        }),
        ('Audit', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )