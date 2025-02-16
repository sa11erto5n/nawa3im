from .generic import *
from django.utils.translation import gettext_lazy as _

@login_required
def UserProfile(request):
    return render(request,'user/profile.html')


@login_required
def EditUserProfile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        thumbnail = request.FILES.get('thumbnail')

        errors = {}
        
        if not first_name:
            errors['first_name'] = _('First name is required.')
        if not last_name:
            errors['last_name'] = _('Last name is required.')
        if not email:
            errors['email'] = _('Email is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Update user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if thumbnail:
            user.profile.image = thumbnail  # Adjust this line as per your user model
        user.save()

        return JsonResponse({'success': True, 'message': 'Profile updated successfully!'})


    return render(request, 'user/edit.html')