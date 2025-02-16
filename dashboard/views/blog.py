from django.shortcuts import render, redirect
from dashboard.models.blog import Blog
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from .generic import *

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/list.html', {'blogs': blogs})

def create(request):
    if request.method == 'POST':
        title_ar = request.POST.get('title_ar')
        title_fr = request.POST.get('title_fr')
        content_ar = request.POST.get('content_ar')
        content_fr = request.POST.get('content_fr')
        image = request.FILES.get('thumbnail')
        errors = {}
        # Validate inputs

        if not image:
            errors['image'] = _('Image is required.')
        if not title_ar:
            errors['title_ar'] = _('Arabic title is required.')
        if not title_fr:
            errors['title_fr'] = _('French title is required.')
        if not content_ar:
            errors['content_ar'] = _('Arabic content is required.')
        if not content_fr:
            errors['content_fr'] = _('French content is required.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        else:
            # Create a new Blog object
            blog = Blog(
                image=image,
                title_ar=title_ar,
                title_fr=title_fr,
                content_ar=content_ar,
                content_fr=content_fr
            )
            blog.save()
            return JsonResponse({
                'success': True,
                'message': _('Blog created successfully!'),
                'redirect_url': reverse_lazy('dash:blogList')
            })
    else:
        return JsonResponse({'success': False, 'error': _('Invalid request method')}, status=405)

class Delete(mixins.AdminOnlyMixin, BaseDeleteView):
    model = Blog 