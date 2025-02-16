from frontend.models.order import Order, OrderItem
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from frontend.models.order import Order
from django.contrib.auth.decorators import login_required
from dashboard.models.country import Commune
from .generic import *

@login_required
def List(request):
    orders = Order.objects.all().order_by('-created_at').select_related(
        'customer', 'wilaya'
    )
    return render(request, 'order/order.html', {
        'orders': orders,
    })

@login_required
def ShipOrder(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        if order.status == 'Pending':
            order.status = 'Shipped'
            order.save()
            return JsonResponse({
                'success': True,
                'message': _('Order shipped successfully!')
            })
        return JsonResponse({
            'success': False,
            'error': _('Order cannot be shipped from its current status!')
        })
    return JsonResponse({
        'success': False,
        'error': _('Invalid request method!')
    })

@login_required
def UpdateOrderStatus(request, pk):
    """New view to handle all status updates"""
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            return JsonResponse({
                'success': True,
                'message': _('Order status updated successfully!')
            })
        return JsonResponse({
            'success': False,
            'error': _('Invalid status provided!')
        })
    return JsonResponse({
        'success': False,
        'error': _('Invalid request method!')
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order,
        pk=pk,
        customer__user=request.user  # Ensure user can only view their own orders
    )
    commune = Commune.objects.get(pk=order.city)
    context = {
        'order': order,
        'commune':commune
    }
    return render(request, 'order/details.html', context=context)


class Delete(mixins.AdminOnlyMixin,BaseDeleteView):
    model = Order