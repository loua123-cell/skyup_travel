from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone_number', 'start_date', 'end_date', 'email']
        labels = {
            'full_name': _("Full Name"),
            'phone_number': _("Phone Number"),
            'start_date': _("Start Date"),
            'end_date': _("End Date"),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})