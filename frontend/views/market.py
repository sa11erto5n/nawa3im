from django.shortcuts import render, redirect
from dashboard.models import Product, Category  # Use PascalCase for class names

def home(request):
    context = {}
    context['categories'] = Category.objects.all()
    return render(request, 'frontend/market/home.html', context=context)

def categoryDetails(request, pk):
    context = {}
    context['category'] = Category.objects.get(pk=pk)
    return render(request, 'frontend/market/category.html', context=context)

def ProductDetails(request, pk):
    context = {}
    context['product'] = Product.objects.get(pk=pk)
    return render(request, 'frontend/market/product.html', context=context)

def search(request):
    if request.method == 'POST':
        query = request.POST.get('q', '').strip()
        if query:
            # Search in product name and description
            results = Product.objects.filter(
                name_ar__icontains=query
            ) | Product.objects.filter(name_fr__icontains=query) | Product.objects.filter(
                description_fr__icontains=query
            ) | Product.objects.filter(description_ar__icontains=query)
            context = {
                'query': query,
                'results': results
            }
            return render(request, 'frontend/market/search_results.html', context=context)
        return render(request, 'frontend/market/search_results.html', {'query': ''})
    return redirect('frontend:home')
