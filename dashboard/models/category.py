from django.db import models
from django.utils import translation

class Category(models.Model):
    image = models.ImageField(upload_to='categories', max_length=None, default='')
    name_ar = models.CharField(max_length=100, blank=True, null=True)
    name_fr = models.CharField(max_length=100, blank=True, null=True)
    description_ar = models.TextField(blank=True, null=True)
    description_fr = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        lang = translation.get_language()
        if lang == 'ar' and self.name_ar:
            return self.name_ar
        if lang == 'fr' and self.name_fr:
            return self.name_fr
        return self.name_ar or self.name_fr or str(self.pk)  # Fallback to first available name or ID

