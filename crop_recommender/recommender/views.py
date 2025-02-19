from django.shortcuts import render
from django.http import JsonResponse
from .models import SoilData, CropInfo
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

def load_model():
    model_path = 'recommender/ml_model/crop_model.joblib'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

def home(request):
    return render(request, 'recommender/home.html')

def predict_crop(request):
    if request.method == 'POST':
        # Get form data
        nitrogen = float(request.POST.get('nitrogen'))
        phosphorus = float(request.POST.get('phosphorus'))
        potassium = float(request.POST.get('potassium'))
        temperature = float(request.POST.get('temperature'))
        humidity = float(request.POST.get('humidity'))
        ph = float(request.POST.get('ph'))
        rainfall = float(request.POST.get('rainfall'))

        # Create feature array
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        
        # Load model and make prediction
        model = load_model()
        if model:
            prediction = model.predict(features)[0]
        else:
            # Fallback logic if model is not available
            prediction = get_recommendation_by_rules(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)

        # Save the data
        soil_data = SoilData.objects.create(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            recommended_crop=prediction
        )

        # Get crop information
        try:
            crop_info = CropInfo.objects.get(name=prediction)
            crop_details = {
                'name': crop_info.name,
                'season': crop_info.season,
                'market_demand': crop_info.market_demand,
                'temperature_range': f"{crop_info.min_temperature}°C - {crop_info.max_temperature}°C",
                'rainfall_range': f"{crop_info.min_rainfall}mm - {crop_info.max_rainfall}mm",
                'ideal_soil_ph': crop_info.ideal_soil_ph
            }
        except CropInfo.DoesNotExist:
            crop_details = None

        return render(request, 'recommender/result.html', {
            'prediction': prediction,
            'crop_details': crop_details,
            'soil_data': soil_data
        })

    return render(request, 'recommender/predict.html')

def get_recommendation_by_rules(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    """Simple rule-based recommendation system as fallback"""
    if temperature > 30 and rainfall < 100:
        return "Cotton"
    elif temperature > 25 and ph > 6:
        return "Rice"
    elif nitrogen > 40 and phosphorus > 40:
        return "Wheat"
    else:
        return "Maize"

def market_analysis(request):
    crops = CropInfo.objects.all()
    return render(request, 'recommender/market.html', {'crops': crops})
