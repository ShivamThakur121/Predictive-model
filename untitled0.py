# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oL6rFCgawiEqxApQDAyxmnyuuysk3UNn
"""

import pandas as pd
import kagglehub

path = kagglehub.dataset_download("shashanknecrothapa/ames-housing-dataset")

df=pd.read_csv("/content/AmesHousing.csv")

df.head()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

numeric_df = df.select_dtypes(include=['number'])
df.fillna(numeric_df.median(), inplace=True)

df = pd.get_dummies(df, drop_first=True)

X = df.drop('SalePrice', axis=1)
y = df['SalePrice']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

rf_model = RandomForestRegressor(random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Predict
y_pred = rf_model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Absolute Error: {mae}')
print(f'R^2 Score: {r2}')

grid_search = GridSearchCV(rf_model, param_grid, cv=3, scoring='neg_mean_absolute_error', verbose=1)
grid_search.fit(X_train, y_train)

# Best parameters
print(f'Best parameters: {grid_search.best_params_}')

from sklearn.model_selection import GridSearchCV

# Feature importance
import matplotlib.pyplot as plt

importances = rf_model.feature_importances_
sorted_indices = importances.argsort()

# Plot
plt.figure(figsize=(10, 6))
plt.barh(range(len(importances)), importances[sorted_indices], align='center')
plt.yticks(range(len(importances)), X.columns[sorted_indices])
plt.xlabel('Feature Importance')
plt.title('Feature Importance in Random Forest')
plt.show()

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

import joblib

# Save the model
joblib.dump(rf_model, 'house_price_model.pkl')

# To load the model later:
# loaded_model = joblib.load('house_price_model.pkl')