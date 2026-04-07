from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True, null=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, blank=True, null=True)

    is_client = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    start_date = models.DateField(_("Departure Date"), null=True, blank=True)
    end_date = models.DateField(_("End Date"), null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")