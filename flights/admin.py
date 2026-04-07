# flights/admin.py
from django.contrib import admin
from .models import Flight, Airport

# Si vous avez un modèle Airport, enregistrez-le aussi
@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('city', 'name', 'code')
    search_fields = ('city', 'code')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste des vols (Mises à jour pour inclure les escales)
    list_display = (
        'flight_number', 
        'airline', 
        'departure_airport', 
        'arrival_airport', 
        'price', 
        'is_direct',     # <--- IMPORTANT : Pour voir si c'est direct
        'stops_count',   # <--- IMPORTANT : Nombre d'escales
        'seats_remaining' # <--- IMPORTANT : Pour afficher "X restant(s)"
    )
    
    # Filtres latéraux (Ajout du filtre par type de vol : Direct ou avec Escale)
    list_filter = (
        'is_direct',      # Filtre pour Vols Directs
        'stops_count',    # Filtre par nombre d'escales
        'airline', 
        'departure_airport', 
        'arrival_airport'
    )
    
    # Barre de recherche améliorée
    search_fields = ('flight_number', 'airline', 'departure_airport__city', 'arrival_airport__city')
    
    # Organisation chronologique (Départ le plus proche en premier)
    ordering = ('departure_time',)