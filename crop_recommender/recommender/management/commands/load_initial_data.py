from django.core.management.base import BaseCommand
from recommender.models import CropInfo

class Command(BaseCommand):
    help = 'Load initial crop data for Pakistan'

    def handle(self, *args, **kwargs):
        # Clear existing data
        CropInfo.objects.all().delete()

        # Create crop data
        crops_data = [
            {
                'name': 'Wheat',
                'season': 'Rabi',
                'market_demand': 'High',
                'min_temperature': 10,
                'max_temperature': 25,
                'min_rainfall': 75,
                'max_rainfall': 100,
                'ideal_soil_ph': 6.5,
            },
            {
                'name': 'Rice',
                'season': 'Kharif',
                'market_demand': 'High',
                'min_temperature': 22,
                'max_temperature': 35,
                'min_rainfall': 100,
                'max_rainfall': 200,
                'ideal_soil_ph': 6.0,
            },
            {
                'name': 'Cotton',
                'season': 'Kharif',
                'market_demand': 'High',
                'min_temperature': 21,
                'max_temperature': 35,
                'min_rainfall': 50,
                'max_rainfall': 100,
                'ideal_soil_ph': 6.5,
            },
            {
                'name': 'Sugarcane',
                'season': 'Kharif',
                'market_demand': 'Medium',
                'min_temperature': 20,
                'max_temperature': 35,
                'min_rainfall': 150,
                'max_rainfall': 250,
                'ideal_soil_ph': 6.5,
            },
            {
                'name': 'Maize',
                'season': 'Both',
                'market_demand': 'Medium',
                'min_temperature': 15,
                'max_temperature': 30,
                'min_rainfall': 60,
                'max_rainfall': 110,
                'ideal_soil_ph': 6.0,
            },
            {
                'name': 'Chickpea',
                'season': 'Rabi',
                'market_demand': 'Medium',
                'min_temperature': 15,
                'max_temperature': 25,
                'min_rainfall': 40,
                'max_rainfall': 80,
                'ideal_soil_ph': 6.5,
            },
            {
                'name': 'Mung Bean',
                'season': 'Kharif',
                'market_demand': 'Medium',
                'min_temperature': 20,
                'max_temperature': 35,
                'min_rainfall': 60,
                'max_rainfall': 100,
                'ideal_soil_ph': 6.5,
            },
            {
                'name': 'Lentil',
                'season': 'Rabi',
                'market_demand': 'Medium',
                'min_temperature': 15,
                'max_temperature': 25,
                'min_rainfall': 40,
                'max_rainfall': 80,
                'ideal_soil_ph': 6.0,
            },
        ]

        for crop_data in crops_data:
            CropInfo.objects.create(**crop_data)

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial crop data'))
