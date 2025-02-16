from django.db import models
from django.conf import settings

class Testimony(models.Model):
    image = models.ImageField(max_length=1200, default='', upload_to='testimony/', verbose_name='Testimony Image')
    fullname_fr = models.CharField(max_length=100)
    fullname_ar = models.CharField(max_length=100)
    content_fr = models.TextField()
    content_ar = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimony by {self.user.username}"

    class Meta:
        verbose_name_plural = "Testimonies"
        ordering = ['-created_at'] 