from django.urls import path
from . import views

# Nom de l'application pour utiliser les namespaces dans les templates (ex: {% url 'cars:car_list' %})
app_name = 'cars'

urlpatterns = [
    # Liste des véhicules (Page d'accueil de l'application)
    path('', views.car_list, name='car_list'),
    
    # Détails d'un véhicule spécifique
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    
    # Espace Administration - Dashboard
    path('management/dashboard/', views.dashboard, name='dashboard'),
    
    # Action : Supprimer une réservation
    path('management/booking/delete/<int:pk>/', views.delete_booking, name='delete_booking'),
]