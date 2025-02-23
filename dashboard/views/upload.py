from django.core.files.storage import default_storage
from django.http import JsonResponse
import uuid
import os

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image = request.FILES['image']
            # Generate unique filename
            ext = os.path.splitext(image.name)[1]
            filename = f"{uuid.uuid4()}{ext}"
            
            # Save file using default storage
            filepath = default_storage.save(f'uploads/{filename}', image)
            
            # Return the full URL path
            return JsonResponse({
                'image_path': filepath,
                'image_url': default_storage.url(filepath)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)