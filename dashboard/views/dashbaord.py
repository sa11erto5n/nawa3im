from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from frontend.models import order,customer
from dashboard.models import category, product 

@login_required
def home(request):
    context = {
        "orders" : order.Order.objects.all(),
        "categories" : category.Category.objects.all(),
        "products" : product.Product.objects.all()
    }
    return render(request,template_name='dashboard/home.html',context=context)