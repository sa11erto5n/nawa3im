from django.http import JsonResponse
from dashboard.models.country import wilaya, Commune
from dashboard.models.shipping import Shipping
import logging

logger = logging.getLogger(__name__)

def get_cities(request, wilaya_code):
    print(True)
    try:
        chosen_wilaya = wilaya.objects.get(code=wilaya_code)
        cities = Commune.objects.filter(wilaya=chosen_wilaya).values()
        logger.debug(f"Found {len(cities)} cities for wilaya {wilaya_code}")
        return JsonResponse(list(cities), safe=False)
    except wilaya.DoesNotExist:
        logger.warning(f"Wilaya with code {wilaya_code} not found")
        return JsonResponse({'error': 'Wilaya not found'}, status=404)
    except Exception as e:
        logger.error(f"Error fetching cities for wilaya {wilaya_code}: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
