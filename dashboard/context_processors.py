from .models.notifications import Notifications
from .models.user import UserProfile
def getUserData(request):
    user = request.user
    if user.is_authenticated:
        userProfile = UserProfile.objects.filter(user=user).first()
        is_admin = user.is_superuser
        return {
            'user':user,
            'is_admin' : is_admin,
            'user_profile':userProfile,
            'notifications' : Notifications.objects.filter(user=user),
        }
    else:
        return {}