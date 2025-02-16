from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from dashboard.models import product
from dashboard.models import country
from . import customer

UserModal = get_user_model()

class Order(models.Model):
    customer = models.ForeignKey(
        customer.Customer, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Customer")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    total_price = models.DecimalField(_("Total Price"), max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=[
            ('Pending', _("Pending")),
            ('Shipped', _("Shipped")),
            ('Delivered', _("Delivered")),
            ('Cancelled', _("Cancelled")),
        ],
        default='Pending',
    )
    payment_method = models.CharField(_("Payment Method"), max_length=50, default=_("Cash on Delivery"))

    # Shipping Details
    full_name = models.CharField(_("Full Name"), max_length=100)
    phone_number = models.CharField(_("Phone Number"), max_length=10)
    wilaya = models.ForeignKey(country.wilaya, on_delete=models.DO_NOTHING, verbose_name=_("Wilaya"))
    city = models.CharField(_("City"), max_length=100)
    shipping_location = models.CharField(
        _("Shipping Location"),
        max_length=10,
        choices=[
            ('home', _("Home")),
            ('office', _("Office")),
        ],
        default='home'
    )
    country = models.CharField(_("Country"), max_length=50, default="Algeria")

    def __str__(self):
        return f"{_('Order')} #{self.id} - {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', verbose_name=_("Order")
    )
    product = models.ForeignKey(
        product.Product, on_delete=models.CASCADE, verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(_("Quantity"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
