# bookings/forms.py
from django import forms
from .models import Booking

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']
        widgets = {
            # Utilisation de widgets de type "date" pour un affichage calendrier
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control rounded-pill'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control rounded-pill'}),
        }