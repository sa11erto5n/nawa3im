from django.core.management.base import BaseCommand
from dashboard.models.country import wilaya, Commune
from django.conf import settings
import json

class Command(BaseCommand):
    help = 'Initialize communes data'
    data = []

    with open(settings.COMMUNES_JSON_PATH, 'r') as f:
        data = json.load(f)
        
    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0
        
        for commune_data in self.data:
            wilaya_obj, _ = wilaya.objects.get_or_create(
                code=commune_data['wilaya_id']
            )
            
            commune_obj, created = Commune.objects.get_or_create(
                post_code=commune_data['post_code'],
                name_fr=commune_data['name'],
                name_ar=commune_data['ar_name'],
                wilaya=wilaya_obj,
            )
            
            if created:
                created_count += 1
            else:
                existing_count += 1
                self.stdout.write(f"Commune already exists: {commune_data['post_code']} - {commune_data['name']}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {created_count} communes'))
        self.stdout.write(self.style.WARNING(f'{existing_count} communes already existed'))