from django.db import models

class SoilData(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    recommended_crop = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Soil Data {self.created_at}"

class CropInfo(models.Model):
    name = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    market_demand = models.CharField(max_length=20)  # High, Medium, Low
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_rainfall = models.FloatField()
    max_rainfall = models.FloatField()
    ideal_soil_ph = models.FloatField()
    
    def __str__(self):
        return self.name
