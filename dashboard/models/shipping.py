from django.db import models
from django.utils.translation import gettext_lazy as _ 
from .country import wilaya

class Shipping(models.Model):
    wilaya = models.OneToOneField(wilaya, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name