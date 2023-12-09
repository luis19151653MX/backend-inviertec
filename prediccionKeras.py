import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import keras

import yfinance as yf

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,GRU

#Cargar los datos
company = 'GOOGL'
ticker = yf.Ticker(company)
hist = ticker.history(start = '2012-1-1', end='2022-12-31')

#Cargar los datos del test
hist_test = ticker.history(start = '2023-1-1', end='2023-10-31')

actual_prices = hist_test["Close"].values
hist_test
prediction_days = 60

#Agregar los 30 días
from datetime import timedelta

# Supongamos que tienes un DataFrame llamado 'df' con las columnas que mencionaste.
hist_test1=hist_test.reset_index();
# Asegúrate de que la columna 'Date' esté en el formato correcto.
hist_test1['Date'] = pd.to_datetime(hist_test1['Date'], format='%Y-%m-%d %H:%M:%S%z')

# Encuentra la última fecha en el DataFrame.
ultima_fecha = hist_test1['Date'].max()
print(ultima_fecha)

#### Calcula la fecha 30 días después.
nueva_fecha = ultima_fecha + timedelta(days=30)
print(nueva_fecha)

# Filtra el DataFrame para obtener las últimas 30 filas (días) y copiarlas a las filas de los próximos 30 días.
ultimos_30_dias = hist_test1[hist_test1['Date'] >= ultima_fecha - timedelta(days=39)]
print(ultima_fecha - timedelta(days=39))
# Actualiza las fechas de los próximos 30 días.
ultimos_30_dias['Date'] = pd.date_range(start=ultima_fecha + timedelta(days=1), periods=28, freq='D')

# Concatena el DataFrame original con los datos de los últimos 30 días.
df_extendido = pd.concat([hist_test1, ultimos_30_dias], ignore_index=True)

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(hist['Close'].values.reshape(-1,1))

total_dataset = pd.concat((hist['Close'],df_extendido['Close']),axis=0)
model_inputs = total_dataset[len(total_dataset)-len(df_extendido)-prediction_days:].values
model_inputs = scaler.transform(model_inputs.reshape(-1,1))

x_test = []

for x in range(prediction_days,len(model_inputs)):
  x_test.append(model_inputs[x-prediction_days:x,0])

x_test = np.array(x_test)
x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))
#Aqui se abre el modelo que ya se tenia creado previamente
model = keras.models.load_model('prediccion_acciones.h5')

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)
#len(predicted_prices)

fechas = df_extendido.set_index("Date")['2023':].iloc[:,0].index.array
#len(fechas)

datosPrediccion=dict(zip(fechas,predicted_prices))
datosPrediccionDF=pd.DataFrame(datosPrediccion).transpose()


actual=dict(zip(fechas,actual_prices))
actual_pricesDF=pd.DataFrame(actual,index=[0]).transpose()
datosPrediccionDF

plt.figure(figsize=(10,6))
plt.plot(actual_pricesDF,color="purple",label=f"{company} real prices")
plt.plot(datosPrediccionDF,color="blue",label=f"{company} predicted prices")
plt.xticks(rotation=90)
plt.legend()
plt.show()