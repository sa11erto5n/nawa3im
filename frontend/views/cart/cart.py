from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from frontend.models.cart import Cart, CartItem
from frontend.models.customer import Customer
from dashboard.models.product import Product
from dashboard.models.country import wilaya
import uuid
from frontend.models.order import Order, OrderItem
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

def get_or_create_cart(request):
    """
    Helper function to get or create a cart for the current user (authenticated or anonymous).
    """
    if request.user.is_authenticated:
        # For authenticated users, link the cart to the Customer
        customer, created = Customer.objects.get_or_create(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
    else:
        # For anonymous users, use the session ID
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        customer, created = Customer.objects.get_or_create(session_id=session_id)
        cart, created = Cart.objects.get_or_create(customer=customer)
    return cart

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided

    cart = get_or_create_cart(request)  # Use the helper function to get or create the cart

    # Add or update the product in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    # Get product name based on current language
    product_name = str(product)

    return JsonResponse({
        'success': True,
        'message': _(f'{quantity} x {product_name} added to cart.'),
    })

def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            # Get the cart directly instead of using request.cart
            item = CartItem.objects.get(pk=item_id)
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                item.quantity = quantity
                item.save()
                
                # Calculate cart totals
                cart = item.cart
                cart_items = cart.items.all()
                total_items = sum(item.quantity for item in cart_items)
                subtotal = sum(item.product.price * item.quantity for item in cart_items)
                shipping_cost = 0  # You can add shipping calculation logic here if needed
                total_amount = subtotal + shipping_cost
                
                return JsonResponse({
                    'success': True,
                    'total_items': total_items,
                    'subtotal': subtotal,
                    'shipping_cost': shipping_cost,
                    'total_amount': total_amount
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid quantity'}, status=400)
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=500)
        
@require_POST
def remove_from_cart(request, cart_item_id):
    """
    Remove a specific cart item from the cart.
    """
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    # Get product name based on current language
    product_name = str(cart_item.product)
    cart_item.delete()

    return JsonResponse({
        'success': True,
        'message': f'{product_name} removed from cart.',
    })

def view_cart(request):
    """
    Display the contents of the cart.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.all().select_related('product')  # Optimize with select_related
    
    # Calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping_price = 0  # Will be calculated based on wilaya
    total = subtotal + shipping_price

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'wilayas': wilaya.objects.all(),
        'subtotal': subtotal,
        'shipping_price': shipping_price,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)

@require_POST
@transaction.atomic
def create_order(request):
    """
    Create an order from the cart contents.
    """
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        return JsonResponse({
            'success': False,
            'error': _('Your cart is empty!')
        })

    # Get shipping details from POST data
    shipping_data = {
        'full_name': request.POST.get('full-name'),
        'phone_number': request.POST.get('phone'),
        'wilaya_id': request.POST.get('wilaya'),
        'city': request.POST.get('city'),
        'shipping_location': request.POST.get('shipping_location', 'home'),
    }

    # Create the order
    try:
        # For authenticated users, get the customer
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
        else:
            customer = Customer.objects.get(session_id=request.session.session_key)

        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = Order.objects.create(
            customer=customer,
            total_price=total_price,
            **shipping_data
        )

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the cart
        cart.items.all().delete()

        return JsonResponse({
            'success': True,
            'message': _('Order created successfully!'),
            'order_id': order.id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })