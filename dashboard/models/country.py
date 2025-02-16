from django.db import models
from django.utils import translation


class wilaya(models.Model):
    code = models.IntegerField()
    name_fr = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.name_ar
        return self.name_fr

    
class Commune(models.Model):
    post_code = models.CharField(max_length=5)
    name_fr = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    wilaya = models.ForeignKey(wilaya, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        lang = translation.get_language()
        if lang == 'ar':
            return self.name_ar
        if lang == 'fr':
            return self.name_fr
    