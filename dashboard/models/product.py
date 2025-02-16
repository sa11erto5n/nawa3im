from django.utils.translation import gettext_lazy as _
from django.utils import translation
from django.db import models
from . import category
from tinymce.models import HTMLField

class Product(models.Model):
    name_ar = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255)
    image = models.ImageField(max_length=1200, default='', upload_to='product/', verbose_name='Product Image')
    description_ar = HTMLField()
    description_fr = HTMLField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        category.Category, on_delete=models.CASCADE, related_name='products', verbose_name=_("Category")
    )
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.name_ar 
        if lang == 'fr':
            return self.name_fr
