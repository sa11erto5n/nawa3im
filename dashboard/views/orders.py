from frontend.models.order import Order
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

def List(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'order/order.html', {'orders': orders})

def ShipOrder(request,pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        order.status = 'Shipped'
        order.save()
        return JsonResponse({'success': True,
                            'message' : _('Order shipped successfully!')}) 
    else:
        return JsonResponse({'success': False,
                            'error' : _('Invalid request method!')})