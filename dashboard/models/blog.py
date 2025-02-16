from django.db import models
from tinymce.models import HTMLField

class Blog(models.Model):
    image = models.ImageField(max_length=1200, default='', upload_to='blog/', verbose_name='Blog Image')
    title_fr = models.CharField(max_length=200)
    title_ar = models.CharField(max_length=200)
    content_fr = HTMLField()
    content_ar = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blog: {self.title_fr}"

    class Meta:
        verbose_name_plural = "Blogs"
        ordering = ['-created_at'] 