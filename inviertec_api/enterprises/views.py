from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
import yfinance as yf
from datetime import date, timedelta

@api_view(['GET'])
def obtener_datos_empresa(request, nombre_empresa):
    try:
        ticker = yf.Ticker(nombre_empresa)
        today = date.today()
        start_date = today - timedelta(days=365 * 2)
        data = ticker.history(start=start_date, end=today)
        data = data.reset_index()
        data = data[['Date', 'Close']]
        data.columns = ['fecha', 'precio']
        data = data.to_dict(orient='records')
        return Response(data)

    except Exception as e:
        return Response({'error': str(e)})
