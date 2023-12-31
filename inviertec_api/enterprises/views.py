#The next 2 linea are to disable warning decrepted messages from keras and TensorFlow
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import yfinance as yf

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pandas as pd
from datetime import date, timedelta, datetime
import keras
import numpy as np
from sklearn.preprocessing import MinMaxScaler


empresas = [
    {'idEnterprise': 1, 'nameEnterprise': 'Apple Inc.', 'ticker': 'AAPL', 'image': 'http://127.0.0.1:3000/images/enterprises/aapl.png'},
    {'idEnterprise': 2, 'nameEnterprise': 'Microsoft Corporation', 'ticker': 'MSFT', 'image': 'http://127.0.0.1:3000/images/enterprises/msft.png'},
    {'idEnterprise': 3, 'nameEnterprise': 'Amazon.com Inc.', 'ticker': 'AMZN', 'image': 'http://127.0.0.1:3000/images/enterprises/amzn.png'},
    {'idEnterprise': 4, 'nameEnterprise': 'Alphabet Inc.', 'ticker': 'GOOGL', 'image': 'http://127.0.0.1:3000/images/enterprises/googl.png'},
    {'idEnterprise': 5, 'nameEnterprise': 'Meta Platforms, Inc.', 'ticker': 'META', 'image': 'http://127.0.0.1:3000/images/enterprises/meta.png'},
    {'idEnterprise': 6, 'nameEnterprise': 'Tesla, Inc.', 'ticker': 'TSLA', 'image': 'http://127.0.0.1:3000/images/enterprises/tsla.png'},
    {'idEnterprise': 7, 'nameEnterprise': 'Johnson & Johnson', 'ticker': 'JNJ', 'image': 'http://127.0.0.1:3000/images/enterprises/jnj.png'},
    {'idEnterprise': 8, 'nameEnterprise': 'Procter & Gamble Co.', 'ticker': 'PG', 'image': 'http://127.0.0.1:3000/images/enterprises/pg.png'},
    {'idEnterprise': 9, 'nameEnterprise': 'JPMorgan Chase & Co.', 'ticker': 'JPM', 'image': 'http://127.0.0.1:3000/images/enterprises/jpm.png'},
    {'idEnterprise': 10, 'nameEnterprise': 'Starbucks Corporation', 'ticker': 'SBUX', 'image': 'http://127.0.0.1:3000/images/enterprises/sbux.png'},
    {'idEnterprise': 11, 'nameEnterprise': 'Exxon Mobil Corporation', 'ticker': 'XOM', 'image': 'http://127.0.0.1:3000/images/enterprises/xom.png'},
    {'idEnterprise': 12, 'nameEnterprise': 'Chevron Corporation', 'ticker': 'CVX', 'image': 'http://127.0.0.1:3000/images/enterprises/cvx.png'},
    {'idEnterprise': 13, 'nameEnterprise': 'Pfizer Inc.', 'ticker': 'PFE', 'image': 'http://127.0.0.1:3000/images/enterprises/pfe.png'},
    {'idEnterprise': 14, 'nameEnterprise': 'The Coca-Cola Company', 'ticker': 'KO', 'image': 'http://127.0.0.1:3000/images/enterprises/ko.png'},
    {'idEnterprise': 15, 'nameEnterprise': 'Intel Corporation', 'ticker': 'INTC', 'image': 'http://127.0.0.1:3000/images/enterprises/intc.png'},
    {'idEnterprise': 16, 'nameEnterprise': 'Boeing Company', 'ticker': 'BA', 'image': 'http://127.0.0.1:3000/images/enterprises/ba.png'},
    {'idEnterprise': 17, 'nameEnterprise': 'Walt Disney Company', 'ticker': 'DIS', 'image': 'http://127.0.0.1:3000/images/enterprises/dis.png'},
    {'idEnterprise': 18, 'nameEnterprise': 'IBM', 'ticker': 'IBM', 'image': 'http://127.0.0.1:3000/images/enterprises/ibm.png'},
    {'idEnterprise': 19, 'nameEnterprise': 'Visa Inc.', 'ticker': 'V', 'image': 'http://127.0.0.1:3000/images/enterprises/v.png'},
    {'idEnterprise': 20, 'nameEnterprise': 'Cisco Systems, Inc.', 'ticker': 'CSCO', 'image': 'http://127.0.0.1:3000/images/enterprises/csco.png'},
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
def predecirValor(request,ticker):
    #mensaje = f"valor de {ticker} para los próximos {dias_predecir} días"
    #calcular fecha actual
    today = datetime.today()
    end_date_str = today.strftime('%Y-%m-%d')

    #cargar los datos
    tickerEnterprise = yf.Ticker(ticker)
    hist = tickerEnterprise.history(start = '2012-1-1', end='2022-12-31')
    hist_test=tickerEnterprise.history(start='2023-1-1', end=end_date_str)
    actual_prices = hist_test["Close"].values
    #crear data frame y dar formato a la fecha
    hist_test1=hist_test.reset_index();
    hist_test1['Date'] = pd.to_datetime(hist_test1['Date'], format='%Y-%m-%d %H:%M:%S%z')


    #fecha a predecir en base a dias_predecir
    prediction_days = 60
    ultima_fecha = hist_test1['Date'].max()

    #obtener datos de los utlimos dias en espejo a los dias_predecir
    ultimos_30_dias = hist_test1[hist_test1['Date'] >= ultima_fecha - timedelta(days=39)]
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

    #Aqui se usa el modelo que ya se tenia creado previamente
    modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modeloPrediccion/modelo_prediccion_acciones.h5'))
    model = keras.models.load_model(modelo_path)
    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)
    

    """
    today = datetime.today().strftime('%Y-%m-%d')
    df_extendido['Date'] = pd.to_datetime(df_extendido['Date']) 
    fechas_filtradas = df_extendido[df_extendido['Date'] >= today]
    fechas = fechas_filtradas['Date'].dt.strftime('%Y-%m-%d').tolist()
    """

    fechas = df_extendido.set_index("Date")['2023':].iloc[:,0].index.array
    data = []
    for fecha, precio in zip(fechas, predicted_prices):
        precio_redondeado = round(float(precio), 2)
        data.append({"date": fecha.strftime('%Y-%m-%d'), "price": precio_redondeado})
    todayFilter = datetime.today().date()
    filtered_data = [item for item in data if datetime.strptime(item["date"], '%Y-%m-%d').date() >= todayFilter]

    return Response(filtered_data)


#to database
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient

def conexion(operacion):
    # Credenciales de MongoDB Atlas
    mongo_uri = 'mongodb+srv://luisgutierrezdev:12345678inviertec@cluster0.djlp14w.mongodb.net/'        # Intentar establecer una conexión con MongoDB Atlas
    client = MongoClient(mongo_uri)
    if(operacion== "open"): 
        # Acceder a la base de datos 'Inviertec'
        db = client.Inviertec
        # Acceder a la colección 'userspredictions' (o el nombre que prefieras)
        coleccion = db.userspredictions
        return coleccion
    if(operacion== "close"):
        client.close()


@csrf_exempt
@api_view(['GET'])
def test_mongo_connection(request):
    try:
        coleccion=conexion("open")
        # Obtener todos los documentos en la colección
        documentos = list(coleccion.find())

        # Convertir ObjectId a str en cada documento
        for doc in documentos:
            doc['_id'] = str(doc['_id'])

        # Cerrar la conexión
        conexion("close")

        # Devolver una respuesta JSON con los documentos recuperados
        return Response({'success': True, 'message': 'Conexión exitosa', 'documentos': documentos})
    except Exception as e:
        # En caso de un error de conexión, devolver una respuesta JSON con el mensaje de error
        return Response({'success': False, 'message': str(e)})
    

@csrf_exempt
@api_view(['POST'])
def guardar_prediccion(request):
    try:
        # Obtener datos del cuerpo de la solicitud POST
        data = request.data
        email = data.get('email')
        empresa=data.get('empresa')
        ticker = data.get('ticker')
        image=data.get('image')
        fecha_registro = datetime.now()
        fecha_prediccion=data.get('fechapred')
        precio_real=data.get('precioreal')
        precio_prediccion=data.get('preciopred')
        acciones=data.get('acciones')
        ganancia=data.get('ganancia')
        real_data = data.get('real_data')
        pred_data = data.get('pred_data')
        visible = data.get('visible', False)

        # Obtener la colección
        coleccion = conexion("open")

        # Crear un nuevo documento
        nuevo_documento = {
            'email': email,
            'empresa': empresa,
            'ticker': ticker,
            'image':image,
            'fechaRegistro': fecha_registro,
            'fecha_prediccion': fecha_prediccion,
            'precio_real': precio_real,
            'precio_prediccion': precio_prediccion,
            'acciones': acciones,
            'ganancia':ganancia,
            'real_data': real_data,
            'pred_data': pred_data,
            'visible': visible
        }

        # Insertar el nuevo documento en la colección
        coleccion.insert_one(nuevo_documento)

        # Cerrar la conexión
        conexion("close")

        return Response({'success': True, 'message': 'Documento agregado correctamente'},status=200)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=400)

@api_view(['GET'])
def obtener_predicciones_email(request, email):
    try:
        # Obtener la colección
        coleccion = conexion("open")

        # Obtener documentos donde 'visible' es True y 'email' coincide
        documentos_visibles = list(coleccion.find({'visible': True, 'email': email}))

        # Convertir ObjectId a str en cada documento
        for doc in documentos_visibles:
            doc['_id'] = str(doc['_id'])

        # Cerrar la conexión
        conexion("close")

        return Response({'success': True, 'message': 'Documentos recuperados correctamente', 'documentos': documentos_visibles})
    except Exception as e:
        return Response({'success': False, 'message': str(e)})