import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

df = pd.read_csv('housing.csv', header=None, names=column_names, delim_whitespace=True)

features = ['CHAS', 'RM', 'TAX', 'PTRATIO', 'B', 'LSTAT']
X = df[features]
y = df['MEDV']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = GradientBoostingRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

score = model.score(X_test_scaled, y_test)
print(f"Model training complete. R2 score: {score:.4f}")

joblib.dump(model, 'boston_housing_prediction.joblib')
print("Model saved to boston_housing_prediction.joblib")

joblib.dump(scaler, 'scaler.joblib')
print("Scaler saved to scaler.joblib")
