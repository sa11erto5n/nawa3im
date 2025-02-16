from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("User")
    )
    session_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Session ID")
    )
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True)
    address = models.TextField(_("Address"), blank=True, null=True)
    city = models.CharField(_("City"), max_length=50, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username
