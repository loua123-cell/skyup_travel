from django.contrib import admin
import time

# Classe de base pour SkyUp Travel
class BaseSkyUpAdmin(admin.ModelAdmin):
    """
    Cette classe gère uniquement le rafraîchissement du cache (Versioning).
    Le style visuel est désormais géré par templates/admin/base_site.html.
    """
    class Media:
        # On utilise un timestamp pour éviter que le navigateur garde l'ancien CSS
        css = {
            'all': (f'admin/css/custom_admin.css?v={time.time()}',)
        }
    
    # NOUS AVONS SUPPRIMÉ changelist_view ET format_html POUR ÉVITER LES ERREURS