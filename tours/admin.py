# skyup_travel/tours/admin.py
from django.contrib import admin
from .models import Tour, ItineraryDay

# Permet d'ajouter les jours du programme directement dans la page du voyage
class ItineraryInline(admin.TabularInline):
    model = ItineraryDay
    extra = 1  # Nombre de lignes vides pour ajouter de nouveaux jours

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    # Gestion de l'affichage du voyage organisé
    inlines = [ItineraryInline]
    list_display = ('title', 'base_price', 'duration_nights')
    search_fields = ('title',)