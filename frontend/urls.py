from django.urls import path,include
from .views import home, market
from .views.cart import cart
from .views.cart import shipping

app_name = 'frontend'

urlpatterns = [
    path('',home.home,name='home'),
    # market
    path('market/',market.home,name='market'),
    # Market Catergories
    path('market/category/<int:pk>/',market.categoryDetails,name='category-details'),
    path('market/search', market.search, name='search'),
    # Market Products
    path('market/product/<int:pk>/',market.ProductDetails,name='product-details'),
    # Cart
    path('cart/', cart.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', cart.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', cart.remove_from_cart, name='remove_from_cart'),

    # Shipping
    path('save-shipping-details/', shipping.save_shipping_details, name='save_shipping_details'),

]

