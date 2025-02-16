from dashboard.models.product import Product 
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from dashboard.models.category import Category
from .generic import *
from dashboard import mixins



@user_passes_test(mixins.is_admin)
def List(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request,'products/list.html',context=context)


@user_passes_test(mixins.is_admin)
def create_product(request):
    errors = {}
    if request.method == 'POST':
        try:
            # Extract data from the form
            name_ar = request.POST.get('name_ar')
            description_ar = request.POST.get('description_ar')
            name_fr = request.POST.get('name_fr')
            description_fr = request.POST.get('description_fr')
            price = request.POST.get('price')
            category_id = request.POST.get('category')
            stock = request.POST.get('stock')
            image = request.FILES.get('thumbnail')

            # Validate inputs
            if not name_ar and name_fr:
                errors['name'] = _('Name is required.')
            if not description_ar and description_fr:
                errors['description'] = _('Description is required.')
            if not price:
                errors['price'] = _('Price is required.')
            if not category_id:
                errors['category'] = _('Category is required.')
            if not stock:
                errors['stock'] = _('Stock is required.')
            if not image:
                errors['image'] = _('Image is required.')
            if errors:
                # Return the form with errors
                return JsonResponse({'success': False, 'errors': errors})
            else:
                # Create the Product object
                category = Category.objects.get(id=category_id)
                product = Product(
                    name_ar=name_ar,
                    description_ar=description_ar,
                    name_fr=name_fr,
                    description_fr=description_fr,
                    price=price,
                    category=category,
                    stock=stock,
                    image=image,
                )
                product.save()

                # Return success response
                return JsonResponse({
                    'success': True,
                    'message': _('Product created successfully!'),
                    'redirect_url': reverse('dash:productsList')
                })
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'error': str(e)}})
    else:
        # Handle GET requests
        context = {
            'categories': Category.objects.all()
        }
        return render(request, 'products/create.html', context=context)
    
class Delete(mixins.AdminOnlyMixin,BaseDeleteView):
    model = Product