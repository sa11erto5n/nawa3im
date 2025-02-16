from django.core.management.base import BaseCommand
from dashboard.models.country import wilaya, Commune
from django.conf import settings
import json

class Command(BaseCommand):
    help = 'Initialize wilayas and communes data'
    wilaya_data = []
    commune_data = []

    with open(settings.WILAYAS_JSON_PATH, 'r') as f:
        wilaya_data = json.load(f)
        
    with open(settings.COMMUNES_JSON_PATH, 'r') as f:
        commune_data = json.load(f)
        
    def handle(self, *args, **options):
        # Initialize wilayas
        wilaya_created = 0
        wilaya_existing = 0
        
        for w_data in self.wilaya_data:
            w_obj, created = wilaya.objects.get_or_create(
                code=w_data['code'],
                name_fr=w_data['name'],
                name_ar=w_data['ar_name'],
                longitude=w_data['longitude'],
                latitude=w_data['latitude']
            )
            
            if created:
                wilaya_created += 1
            else:
                wilaya_existing += 1
                self.stdout.write(f"Wilaya already exists: {w_data['code']} - {w_data['name']}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {wilaya_created} wilayas'))
        self.stdout.write(self.style.WARNING(f'{wilaya_existing} wilayas already existed'))
        
        # Initialize communes
        commune_created = 0
        commune_existing = 0
        
        for c_data in self.commune_data:
            try:
                wilaya_obj = wilaya.objects.get(code=c_data['wilaya_id'])
                c_obj, created = Commune.objects.get_or_create(
                    post_code=c_data['post_code'],
                    name_fr=c_data['name'],
                    name_ar=c_data['ar_name'],
                    wilaya=wilaya_obj
                )
                
                if created:
                    commune_created += 1
                else:
                    commune_existing += 1
                    self.stdout.write(f"Commune already exists: {c_data['id']} - {c_data['name']}")
                    
            except wilaya.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Wilaya not found for commune: {c_data['code']} - {c_data['name']}"))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {commune_created} communes'))
        self.stdout.write(self.style.WARNING(f'{commune_existing} communes already existed'))