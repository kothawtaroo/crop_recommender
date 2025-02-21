# Crop Recommendation System for Pakistani Farmers

A Decision Support System that helps farmers in Pakistan make informed decisions about crop selection based on:
- Soil conditions
- Weather patterns
- Market demand

## Features
- Input soil parameters (N, P, K, pH)
- Get weather data for your region
- View market demand analysis
- Receive crop recommendations using Machine Learning
- User-friendly interface

## Setup Instructions
1. Create a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run migrations:
```
python manage.py makemigrations
python manage.py migrate
```

4. Start the development server:
```
python manage.py runserver
```

5. Visit http://localhost:8000 in your browser

## Technology Stack
- Django
- Scikit-learn (Decision Tree)
- Bootstrap
- SQLite
