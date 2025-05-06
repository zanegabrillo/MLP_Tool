import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pickle

# Load dataset
df = pd.read_csv("calories.csv")
df = df[df["per100grams"] == "100g"]
df["Cals_per100grams"] = df["Cals_per100grams"].str.replace(" cal", "").astype(float)
df["FoodItem"] = df["FoodItem"].str.strip().str.lower()

# Generate synthetic data
synthetic_data = []
for _, row in df.iterrows():
    for _ in range(30):
        grams = np.random.randint(50, 501)
        total_cal = (row["Cals_per100grams"] * grams) / 100
        synthetic_data.append([row["FoodItem"], grams, total_cal])

synthetic_df = pd.DataFrame(synthetic_data, columns=["FoodItem", "Grams", "TotalCalories"])

# One-hot encoding
encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
X_encoded = encoder.fit_transform(synthetic_df[["FoodItem"]])
X = np.concatenate([X_encoded, synthetic_df[["Grams"]].values], axis=1)
y = synthetic_df["TotalCalories"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train MLPRegressor (Neural Network)
model = MLPRegressor(
    hidden_layer_sizes=(128, 64, 32),  # More neurons/layers
    max_iter=1000,
    activation='relu',
    solver='adam',
    random_state=42
)
model.fit(X_train, y_train)

# Save model and encoder
with open("calorie_model.pkl", "wb") as f:
    pickle.dump((model, encoder), f)
