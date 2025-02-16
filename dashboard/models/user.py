from django.db import models
from django.contrib.auth import get_user_model
from .notifications import Notifications

UserModel = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(UserModel,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(max_length=1200,upload_to='user/',verbose_name='User Image')
    notifications_count = models.IntegerField(default=0,verbose_name='User Notifications')
