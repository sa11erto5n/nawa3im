from django.urls import path,include
from .views import auth, customer, dashbaord, notifications, user, products, categories,orders, shipping, testimony, blog, country,ai, upload
app_name = 'dash'

urlpatterns = [
    # auth 
    path('login/',auth.login_view,name='login'),
    path('logout/',auth.logout_view,name='logout'),
    path('home/',dashbaord.home,name='home'),
    # User
    path('user/',user.UserProfile,name='user-profile'),
    path('user/edit/',user.EditUserProfile,name='edit-user-profile'),
    # Products
    path('products/',products.List,name='productsList'),
    path('products/create/',products.create_product,name='create-product'),
    path('products/delete/<int:pk>/',products.Delete.as_view(),name='product-delete'),
    # category
    path('categories/',categories.List,name='categoriesList'),
    path('categories/create/',categories.create,name='category-create'),
    path('categories/delete/<int:pk>/',categories.Delete.as_view(),name='category-delete'),
    # Shipping
    path('shipping/',shipping.List,name='shippingList'),
    path('shipping/create/',shipping.create,name='shipping-create'),
    path('shipping/delete/<int:pk>/',shipping.Delete.as_view(),name='shipping-delete'),
    path('shipping/getShippingPrice/<int:wilaya_id>/', shipping.getShippingPrice, name='get-shipping-price'),
    # testimony
    path('testimony/',testimony.testimony_list,name='testimonyList'),
    path('testimony/create/',testimony.create,name='testimony-create'),
    path('testimony/delete/<int:pk>/',testimony.Delete.as_view(),name='testimony-delete'),
    # Blog URLs
    path('blogs/', blog.blog_list, name='blogList'),
    path('blog/create/', blog.create, name='blog-create'),
    path('blog/delete/<int:pk>/', blog.Delete.as_view(), name='blog-delete'),

    # orders 
    path('orders/',orders.List,name='orderList'),
    path('orders/status/<int:pk>/',orders.ShipOrder,name='shipOrder'),
    path('order/<int:pk>/', orders.order_detail, name='order-detail'),
    path('order/delete/<int:pk>/', orders.Delete.as_view(), name='order-delete'),
    
    # country
    path('api/wilayas/<int:wilaya_code>/cities/', country.get_cities, name='get_cities'),
    
    # AI 
    path('chat/', ai.chat, name='chat_with_ai'),
    path('analyze-image/', ai.analyze_image, name='analyze_image'),
    # upload 
    path('upload-image/', upload.upload_image, name='upload_image'),

]

