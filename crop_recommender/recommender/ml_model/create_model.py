from sklearn.tree import DecisionTreeClassifier
import numpy as np
import joblib
import os

# Create synthetic data
np.random.seed(42)
n_samples = 1000

# Generate random features
N = np.random.normal(50, 20, n_samples)
P = np.random.normal(40, 15, n_samples)
K = np.random.normal(45, 15, n_samples)
temperature = np.random.normal(25, 5, n_samples)
humidity = np.random.normal(70, 10, n_samples)
ph = np.random.normal(6.5, 1, n_samples)
rainfall = np.random.normal(1000, 200, n_samples)

X = np.column_stack([N, P, K, temperature, humidity, ph, rainfall])

# Define some simple rules for crops
crops = []
for i in range(n_samples):
    if temperature[i] > 30 and rainfall[i] < 800:
        crops.append('Cotton')
    elif ph[i] < 6 and rainfall[i] > 1200:
        crops.append('Rice')
    elif N[i] > 60 and P[i] > 50:
        crops.append('Wheat')
    else:
        crops.append('Maize')

y = np.array(crops)

# Train the model
model = DecisionTreeClassifier(random_state=42, max_depth=5)
model.fit(X, y)

# Save the model with absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'crop_model.joblib')
print(f"Saving model to: {model_path}")
joblib.dump(model, model_path)
print("Model saved successfully!")
