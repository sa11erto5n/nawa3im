from django.db import models
from django.utils.translation import gettext_lazy as _
from dashboard.models import product
from . import customer

class Cart(models.Model):
    customer = models.OneToOneField(
        customer.Customer, on_delete=models.CASCADE, verbose_name=_("Customer")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return f"{_('Cart')} - {self.customer.user.username}"

    @property
    def total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items', verbose_name=_("Cart")
    )
    product = models.ForeignKey(
        product.Product, on_delete=models.CASCADE, verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(_("Quantity"),default=1)

    def __str__(self):
        
        return f"{self.quantity} x {self.product.name} in {_('Cart')} {self.cart.customer.user.username}"

    @property
    def item_total(self):
        """
        Calculate the total price for this cart item.
        """
        return self.product.price * self.quantity