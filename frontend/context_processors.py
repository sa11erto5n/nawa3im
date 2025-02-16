from frontend.models.cart import Cart, CartItem
from frontend.models.customer import Customer


def cart_items(request):
    """
    Context processor to add the customer's cart items to the template context.
    """
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, get the customer's cart
        customer, created = Customer.objects.get_or_create(user=request.user)
        cart, created = Cart.objects.get_or_create(customer=customer)
        cart_items = cart.items.all()
    else:
        # For anonymous users, use the session ID to get the cart
        if request.session.session_key:
            session_id = request.session.session_key
            customer, created = Customer.objects.get_or_create(session_id=session_id)
            cart, created = Cart.objects.get_or_create(customer=customer)
            cart_items = cart.items.all()

    return {
        'cart_items': cart_items,
        'cart_total_items': cart_items.count,  # Total number of items in the cart
        'cart_total_price': sum(item.product.price * item.quantity for item in cart_items),  # Total price of items
    }