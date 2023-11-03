# -*- coding: utf-8 -*-
"""Ащимов Арсеній БС-14 КП№4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1elqyjsFIW_pfV9QuzK9nABefwcnOHwGB
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.datasets import fetch_california_housing
from keras.models import Sequential
from keras.layers import Dense, LeakyReLU
from keras import regularizers

# Завантаження California housing data
data = fetch_california_housing()
X = data.data
y = data.target

# Розділення даних на навчальний та тестувальний набори
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Нормалізація даних
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Створення та навчання моделі
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(X_train.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

history = model.fit(X_train, y_train, epochs=100, validation_split=0.2)

# Оцінка якості моделі
test_loss, test_mae = model.evaluate(X_test, y_test)
print(f"\nTest Loss: {test_loss}")
print(f"Mean Absolute Error on Test Data: {test_mae}")

# Прогнозування
y_pred = model.predict(X_test)
print(y_pred[:5])

# Розрахунок середньоквадратичної помилки
mse = mean_squared_error(y_test, y_pred)
print('Mean Squared Error:', mse)

# Експеримент 1: Додавання ще одного прихованого шару та зміна функції активації
model1 = Sequential()
model1.add(Dense(64, activation=LeakyReLU(), input_shape=(X_train.shape[1],)))
model1.add(Dense(64, activation=LeakyReLU()))
model1.add(Dense(1, activation='linear'))

model1.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
history1 = model1.fit(X_train, y_train, epochs=100, validation_split=0.2, verbose=0)

# Експеримент 2: Зміна кількості нейронів та додавання регуляризації
model2 = Sequential()
model2.add(Dense(128, activation='relu', input_shape=(X_train.shape[1],)))
model2.add(Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
model2.add(Dense(1, activation='linear'))

model2.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
history2 = model2.fit(X_train, y_train, epochs=100, validation_split=0.2, verbose=0)

# Оцінка якості моделей для експериментів
test_loss1, test_mae1 = model1.evaluate(X_test, y_test)
test_loss2, test_mae2 = model2.evaluate(X_test, y_test)

print('\nResults of Experiment 1:')
print(f"Test Loss: {test_loss1}")
print(f"Mean Absolute Error on Test Data: {test_mae1}")

print('\nResults of Experiment 2:')
print(f"Test Loss: {test_loss2}")
print(f"Mean Absolute Error on Test Data: {test_mae2}")

# Графіки втрат для експериментів
plt.subplot(2, 2, 1)
plt.plot(history1.history['loss'], label='Train Loss (Exp 1)')
plt.plot(history1.history['val_loss'], label='Validation Loss (Exp 1)')
plt.title(' Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss Value')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(history2.history['loss'], label='Train Loss (Exp 2)')
plt.plot(history2.history['val_loss'], label='Validation Loss (Exp 2)')
plt.title(' Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss Value')
plt.legend()

# Графіки метрик (наприклад, MAE) для експериментів
plt.subplot(2, 2, 3)
plt.plot(history1.history['mae'], label='Training MAE (Exp 1)')
plt.plot(history1.history['val_mae'], label='Validation MAE (Exp 1)')
plt.title(' Training and Validation MAE')
plt.xlabel('Epoch')
plt.ylabel('MAE Value')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(history2.history['mae'], label='Training MAE (Exp 2)')
plt.plot(history2.history['val_mae'], label='Validation MAE (Exp 2)')
plt.title(' Training and Validation MAE')
plt.xlabel('Epoch')
plt.ylabel('MAE Value')
plt.legend()

plt.tight_layout()
plt.show()