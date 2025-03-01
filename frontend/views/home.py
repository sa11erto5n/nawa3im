from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json 
from dashboard.models.product import Product
from dashboard.models.category import Category
from dashboard.models.testimony import Testimony
from dashboard.models.blog import Blog

def home(request):
    context = {}
    context['products'] = Product.objects.all().order_by('-created_at')[:6]
    context['categories'] = Category.objects.all().order_by('-created_at')[:6]
    context['testemonies'] = Testimony.objects.all().order_by('-created_at')[:3]
    context['blogs'] = Blog.objects.all().order_by('-created_at')[:3]
    return render(request, 'frontend/index.html', context=context)

