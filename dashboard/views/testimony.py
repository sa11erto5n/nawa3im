from django.shortcuts import render, redirect
from dashboard.models.testimony import Testimony
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .generic import *

def testimony_list(request):
    testimonies = Testimony.objects.all().order_by('-created_at')
    return render(request, 'testimony/list.html', {'testimonies': testimonies})

def create(request):
    if request.method == 'POST':
        name_ar = request.POST.get('name_ar')
        name_fr = request.POST.get('name_fr')
        description_ar = request.POST.get('description_ar')
        description_fr = request.POST.get('description_fr')
        image = request.FILES.get('thumbnail')
        errors = {}
        # Validate inputs

        if not image:
            errors['image'] = _('Image is required.')
        if not name_ar:
            errors['name_ar'] = _('Arabic name is required.')
        if not name_fr:
            errors['name_fr'] = _('French name is required.')
        if not description_ar:
            errors['description_ar'] = _('Arabic description is required.')
        if not description_fr:
            errors['description_fr'] = _('French description is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            # Create a new Testimony object
            testimony = Testimony(
                image=image,
                fullname_ar=name_ar,
                fullname_fr=name_fr,
                content_ar=description_ar,
                content_fr=description_fr
            )
            testimony.save()
            return JsonResponse({
                'success': True,
                'message': _('Testimony created successfully!'),
                'redirect_url': reverse_lazy('dash:testimonyList')
            })
    else:
        return JsonResponse({'success': False, 'error': _('Invalid request method')}, status=405)

class Delete(mixins.AdminOnlyMixin,BaseDeleteView):
    model = Testimony
