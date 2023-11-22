from django.shortcuts import render

# Create your views here.
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view
import yfinance as yf
from datetime import date, timedelta
import keras


modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modeloPrediccion/modelo_prediccion_acciones.h5'))
model = keras.models.load_model(modelo_path)

empresas = [
    {'idEnterprise': 1, 'nameEnterprise': 'Apple Inc.', 'ticker': 'AAPL', 'image': 'http://127.0.0.1:3002/images/enterprises/aapl.png'},
    {'idEnterprise': 2, 'nameEnterprise': 'Microsoft Corporation', 'ticker': 'MSFT', 'image': 'http://127.0.0.1:3002/images/enterprises/msft.png'},
    {'idEnterprise': 3, 'nameEnterprise': 'Amazon.com Inc.', 'ticker': 'AMZN', 'image': 'http://127.0.0.1:3002/images/enterprises/amzn.png'},
    {'idEnterprise': 4, 'nameEnterprise': 'Alphabet Inc.', 'ticker': 'GOOGL', 'image': 'http://127.0.0.1:3002/images/enterprises/googl.png'},
    {'idEnterprise': 5, 'nameEnterprise': 'Meta Platforms, Inc.', 'ticker': 'META', 'image': 'http://127.0.0.1:3002/images/enterprises/meta.png'},
    {'idEnterprise': 6, 'nameEnterprise': 'Tesla, Inc.', 'ticker': 'TSLA', 'image': 'http://127.0.0.1:3002/images/enterprises/tsla.png'},
    {'idEnterprise': 7, 'nameEnterprise': 'Johnson & Johnson', 'ticker': 'JNJ', 'image': 'http://127.0.0.1:3002/images/enterprises/jnj.png'},
    {'idEnterprise': 8, 'nameEnterprise': 'Procter & Gamble Co.', 'ticker': 'PG', 'image': 'http://127.0.0.1:3002/images/enterprises/pg.png'},
    {'idEnterprise': 9, 'nameEnterprise': 'JPMorgan Chase & Co.', 'ticker': 'JPM', 'image': 'http://127.0.0.1:3002/images/enterprises/jpm.png'},
    {'idEnterprise': 10, 'nameEnterprise': 'Starbucks Corporation', 'ticker': 'SBUX', 'image': 'http://127.0.0.1:3002/images/enterprises/sbux.png'},
    {'idEnterprise': 11, 'nameEnterprise': 'Exxon Mobil Corporation', 'ticker': 'XOM', 'image': 'http://127.0.0.1:3002/images/enterprises/xom.png'},
    {'idEnterprise': 12, 'nameEnterprise': 'Chevron Corporation', 'ticker': 'CVX', 'image': 'http://127.0.0.1:3002/images/enterprises/cvx.png'},
    {'idEnterprise': 13, 'nameEnterprise': 'Pfizer Inc.', 'ticker': 'PFE', 'image': 'http://127.0.0.1:3002/images/enterprises/pfe.png'},
    {'idEnterprise': 14, 'nameEnterprise': 'The Coca-Cola Company', 'ticker': 'KO', 'image': 'http://127.0.0.1:3002/images/enterprises/ko.png'},
    {'idEnterprise': 15, 'nameEnterprise': 'Intel Corporation', 'ticker': 'INTC', 'image': 'http://127.0.0.1:3002/images/enterprises/intc.png'},
    {'idEnterprise': 16, 'nameEnterprise': 'Boeing Company', 'ticker': 'BA', 'image': 'http://127.0.0.1:3002/images/enterprises/ba.png'},
    {'idEnterprise': 17, 'nameEnterprise': 'Walt Disney Company', 'ticker': 'DIS', 'image': 'http://127.0.0.1:3002/images/enterprises/dis.png'},
    {'idEnterprise': 18, 'nameEnterprise': 'IBM', 'ticker': 'IBM', 'image': 'http://127.0.0.1:3002/images/enterprises/ibm.png'},
    {'idEnterprise': 19, 'nameEnterprise': 'Visa Inc.', 'ticker': 'V', 'image': 'http://127.0.0.1:3002/images/enterprises/v.png'},
    {'idEnterprise': 20, 'nameEnterprise': 'Cisco Systems, Inc.', 'ticker': 'CSCO', 'image': 'http://127.0.0.1:3002/images/enterprises/csco.png'},
]

empresas_datos=[]
#@api_view(['GET'])
def cargar_datos_empresas():
    try:
        resultados = []

        for empresa in empresas:
            nombre_empresa = empresa['ticker']
            ticker = yf.Ticker(nombre_empresa)
            data = ticker.history(period='1d')

            if not data.empty and 'Close' in data.columns:
                ultimo_precio_cierre = round(data['Close'].iloc[-1], 2)
            else:
                ultimo_precio_cierre = None

            resultado_empresa = {
                'idEnterprise': empresa['idEnterprise'],
                'nameEnterprise': empresa['nameEnterprise'],
                'ticker': empresa['ticker'],
                'lastPrice': ultimo_precio_cierre,
                'image':empresa['image']
            }
            empresas_datos.append(resultado_empresa)
            resultados.append(resultado_empresa)

        return Response(resultados)

    except Exception as e:
        return Response({'error': str(e)})

@api_view(['GET'])
def obtener_datos_empresas(request):
    return Response(empresas_datos)

@api_view(['GET'])
def obtener_datos_empresa(request, nombre_empresa):
    try:
        ticker = yf.Ticker(nombre_empresa)
        today = date.today()
        start_date = today - timedelta(days=365 * 1)
        data = ticker.history(start=start_date, end=today)
        data = data.reset_index()
        data = data[['Date', 'Close']]
        data.columns = ['date', 'price']
        
         # precio a dos decimales
        data['price'] = data['price'].apply(lambda x: round(x, 2))

        data = data.to_dict(orient='records')
        return Response(data)

    except Exception as e:
        return Response({'error': str(e)})


@api_view(['GET'])
def predecirValor(request,nombre_empresa):
    mensaje = "valor de " + nombre_empresa
    return Response({'mensaje': mensaje})