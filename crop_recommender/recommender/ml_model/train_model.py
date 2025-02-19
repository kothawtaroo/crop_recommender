import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Sample data for Pakistani crops
data = {
    'N': np.random.randint(0, 140, 1000),
    'P': np.random.randint(5, 145, 1000),
    'K': np.random.randint(5, 205, 1000),
    'temperature': np.random.uniform(8.83, 43.68, 1000),
    'humidity': np.random.uniform(14.26, 99.98, 1000),
    'ph': np.random.uniform(3.5, 9.94, 1000),
    'rainfall': np.random.uniform(20.21, 298.56, 1000),
}

# Define conditions for different crops common in Pakistan
def assign_crop(row):
    if row['temperature'] > 30 and row['rainfall'] < 100:
        return 'Cotton'
    elif row['temperature'] > 25 and row['ph'] > 6:
        return 'Rice'
    elif row['N'] > 40 and row['P'] > 40:
        return 'Wheat'
    elif row['temperature'] > 20 and row['humidity'] > 60:
        return 'Sugarcane'
    elif row['ph'] > 6 and row['temperature'] < 30:
        return 'Maize'
    else:
        return np.random.choice(['Chickpea', 'Mung Bean', 'Lentil'])

# Create DataFrame
df = pd.DataFrame(data)
df['crop'] = df.apply(assign_crop, axis=1)

# Prepare features and target
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['crop']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'crop_model.joblib')

# Print model accuracy
print(f"Model accuracy: {model.score(X_test, y_test):.2f}")
