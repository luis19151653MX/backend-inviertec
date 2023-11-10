from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
import yfinance as yf
from datetime import date, timedelta

empresas = [
    {'idEnterprise': 1, 'nameEnterprise': 'Apple Inc.', 'ticker': 'AAPL'},
    {'idEnterprise': 2, 'nameEnterprise': 'Microsoft Corporation', 'ticker': 'MSFT'},
    {'idEnterprise': 3, 'nameEnterprise': 'Amazon.com Inc.', 'ticker': 'AMZN'},
    {'idEnterprise': 4, 'nameEnterprise': 'Alphabet Inc.', 'ticker': 'GOOGL'},
    {'idEnterprise': 5, 'nameEnterprise': 'Facebook, Inc.', 'ticker': 'FB'},
    {'idEnterprise': 6, 'nameEnterprise': 'Tesla, Inc.', 'ticker': 'TSLA'},
    {'idEnterprise': 7, 'nameEnterprise': 'Johnson & Johnson', 'ticker': 'JNJ'},
    {'idEnterprise': 8, 'nameEnterprise': 'Procter & Gamble Co.', 'ticker': 'PG'},
    {'idEnterprise': 9, 'nameEnterprise': 'JPMorgan Chase & Co.', 'ticker': 'JPM'},
    {'idEnterprise': 10, 'nameEnterprise': 'Goldman Sachs Group, Inc.', 'ticker': 'GS'},
    {'idEnterprise': 11, 'nameEnterprise': 'Exxon Mobil Corporation', 'ticker': 'XOM'},
    {'idEnterprise': 12, 'nameEnterprise': 'Chevron Corporation', 'ticker': 'CVX'},
    {'idEnterprise': 13, 'nameEnterprise': 'Pfizer Inc.', 'ticker': 'PFE'},
    {'idEnterprise': 14, 'nameEnterprise': 'The Coca-Cola Company', 'ticker': 'KO'},
    {'idEnterprise': 15, 'nameEnterprise': 'Intel Corporation', 'ticker': 'INTC'},
    {'idEnterprise': 16, 'nameEnterprise': 'Boeing Company', 'ticker': 'BA'},
    {'idEnterprise': 17, 'nameEnterprise': 'Walt Disney Company', 'ticker': 'DIS'},
    {'idEnterprise': 18, 'nameEnterprise': 'IBM', 'ticker': 'IBM'},
    {'idEnterprise': 19, 'nameEnterprise': 'Visa Inc.', 'ticker': 'V'},
    {'idEnterprise': 20, 'nameEnterprise': 'Cisco Systems, Inc.', 'ticker': 'CSCO'},
]

@api_view(['GET'])
def obtener_datos_empresas(request):
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
                'lastPrice': ultimo_precio_cierre
            }

            resultados.append(resultado_empresa)

        return Response(resultados)

    except Exception as e:
        return Response({'error': str(e)})

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
