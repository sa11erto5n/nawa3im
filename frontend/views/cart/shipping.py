from frontend.models.order import Order, OrderItem
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from frontend.views.cart.cart import get_or_create_cart
from dashboard.models.country import wilaya
from dashboard.models.notifications import Notifications
from django.contrib.auth import get_user_model

admin = get_user_model().objects.get(username='admin')

@require_POST
def save_shipping_details(request):
    """
    Save shipping details to the order and proceed to payment.
    """
    # Get the current cart
    cart = get_or_create_cart(request)

    # Validate the form data
    full_name = request.POST.get('full-name')
    phone = request.POST.get('phone')
    wilaya_id = request.POST.get('wilaya')
    city = request.POST.get('city')
    shipping_location = request.POST.get('shipping_location')
    errors = {}

    if not all([full_name, phone, wilaya, city, shipping_location]):
        errors['shipping_details'] = _('Please fill out all shipping details.')

    if errors:
        return JsonResponse({'success': False, 'errors': errors})

    # Create a new order with shipping details
    try:
        chose_wilaya = wilaya.objects.get(id=wilaya_id)
        order = Order.objects.create(
            customer=cart.customer,
            full_name=full_name,
            phone_number=phone,
            wilaya=chose_wilaya,
            city=city,
            shipping_location=shipping_location,
            total_price=cart.total_price,  # Shipping cost will be calculated separately
        )

        # Add cart items to the order
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

        # Clear the cart after creating the order
        cart.items.all().delete()
        Notifications.objects.create(
            user=admin,
            title=_('New Order'),
            text=_('Order #%(order_id)s has been placed.') % {'order_id': order.id}
        )
        return JsonResponse({
            'success': True,
            'message': _('Shipping details saved successfully.'),
            'redirect_url': '/cart/',  # Redirect to the payment page
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {
                'shipping_details': _(f'Failed to save shipping details {str(e)}'),
            },
        })