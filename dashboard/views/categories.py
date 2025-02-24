from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from dashboard.models.category import Category
from .generic import *

@user_passes_test(mixins.is_admin)
def List(request):
    context = {
        'categories': Category.objects.all()
    }
    return render(request, 'categories/list.html', context)

@user_passes_test(mixins.is_admin)
def create(request):
    if request.method == 'POST':
        name_ar = request.POST.get('name_ar')
        description_ar = request.POST.get('description_ar')
        name_fr = request.POST.get('name_fr')
        description_fr = request.POST.get('description_fr')
        image = request.FILES.get('thumbnail')
        errors = {}
        # Validate inputs

        if not image:
            errors['image'] = _('Image is required.')
        if not name_ar or not name_fr:
            errors['name'] = _('Name is required.')
        if not description_ar or not description_fr:
            errors['description'] = _('Description is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            # Create a new Category object
            category = Category(image=image, name_ar=name_ar, description_ar=description_ar , name_fr=name_fr, description_fr=description_fr)
            category.save()
            return JsonResponse({'success': True, 'message': _('Category created successfully!'),'redirect_url': reverse_lazy('dash:categoriesList')})
    else:
        return JsonResponse({'success': False, 'error': _('Invalid request method')}, status=405)
    
    
class Delete(mixins.AdminOnlyMixin,BaseDeleteView):
    model = Category

@user_passes_test(mixins.is_admin)
def edit(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return JsonResponse({'success': False, 'error': _('Category not found')}, status=404)

    if request.method == 'POST':
        name_ar = request.POST.get('name_ar')
        description_ar = request.POST.get('description_ar')
        name_fr = request.POST.get('name_fr')
        description_fr = request.POST.get('description_fr')
        image = request.FILES.get('thumbnail')
        errors = {}
        
        # Validate inputs
        if not name_ar or not name_fr:
            errors['name'] = _('Name is required.')
        if not description_ar or not description_fr:
            errors['description'] = _('Description is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            # Update the Category object
            category.name_ar = name_ar
            category.description_ar = description_ar
            category.name_fr = name_fr
            category.description_fr = description_fr
            if image:  # Only update image if a new one is provided
                category.image = image
            category.save()
            return JsonResponse({'success': True, 'message': _('Category updated successfully!'), 'redirect_url': reverse_lazy('dash:categoriesList')})
    else:
        context = {
            'category': category,
            # Add other context variables as needed
        }
        return render(request, 'categories/edit.html', context)

