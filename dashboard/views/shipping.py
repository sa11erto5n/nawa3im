from django.shortcuts import render ,redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from dashboard.models.shipping import Shipping
from dashboard.models.country import wilaya

from .generic import *

@user_passes_test(mixins.is_admin)
def List(request):
    context = {
        'wilayas': wilaya.objects.all(),
        'objects': Shipping.objects.all()
    }
    return render(request, 'shipping/list.html', context)

@user_passes_test(mixins.is_admin)
def create(request):
    if request.method == 'POST':
        wilaya_id = request.POST.get('wilaya')
        price = request.POST.get('price')
        errors = {}
        # Validate inputs

        if not wilaya_id:
            errors['wilaya'] = _('wilaya is required.')
        if not price:
            errors['price'] = _('pice is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            chosen_wilaya = wilaya.objects.get(id=wilaya_id)
            # Create a new Category object
            shipping = Shipping(wilaya=chosen_wilaya,price=price)
            shipping.save()
            return JsonResponse({'success': True, 'message': _('Shipping created successfully!'),'redirect_url': reverse_lazy('dash:shippingList')})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
class Delete(mixins.AdminOnlyMixin,BaseDeleteView):
    model = Shipping

