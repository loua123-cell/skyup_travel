"""
Configuration des URL pour le projet skyup_travel.

La liste `urlpatterns` route les URL vers les vues.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

# 1. Routes de base (hors préfixes de langue)
# On place généralement le changement de langue ici pour éviter /fr/i18n/
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# 2. Routes avec support international (ajoute /en/, /ar/, /fr/ aux URLs)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    
    # Applications du projet
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('hotels/', include('hotels.urls')),
    path('cars/', include('cars.urls')),
    path('flights/', include('flights.urls')), 
    path('bookings/', include('bookings.urls')),
    
    # Authentification par défaut de Django (Login, Logout, Password Reset)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Si prefix_default_language est True, l'URL sera /fr/ par défaut.
    # Si False, l'URL racine restera / pour la langue par défaut.
    prefix_default_language=True,
)

# 3. Gestion des fichiers média et statiques en mode Développement
# On ajoute également STATIC_URL pour être certain que tout s'affiche en local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)