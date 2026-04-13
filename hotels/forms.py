from django import forms
from .models import HotelBooking
from django.utils.translation import gettext_lazy as _

class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'check_in_date', 'check_out_date', 
                  'number_of_adults', 'number_of_children', 'number_of_babies']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Votre nom complet')
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Votre email')
            }),
            'guest_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Numéro de téléphone')
            }),
            'check_in_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'check_out_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'number_of_adults': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'number_of_children': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'number_of_babies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
