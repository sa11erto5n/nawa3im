from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models.user import UserProfile
from django.core.cache import cache
from rosetta.signals import post_save as rosetta_post_save
from django.core.management import call_command
from django.utils.translation import trans_real

@receiver(post_save,sender=get_user_model())
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            image='images/user-teal.png',
            notifications_count=0,
            
        )


@receiver(rosetta_post_save)
def clear_rosetta_translation_cache(sender, **kwargs):
    """
    Automatically recompile translations and clear the cache
    whenever a .po file is saved via Rosetta.
    """
    # Recompile .po files into .mo files
    call_command('compilemessages')

    # Clear the internal translation cache
    trans_real._translations = {}

    print("Translations recompiled and cache cleared.")

