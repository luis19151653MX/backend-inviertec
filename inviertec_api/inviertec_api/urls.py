from django.contrib import admin
from django.urls import path
from enterprises.views import obtener_datos_empresa;
#from enterprises.views import cargar_datos_empresas;
from enterprises.views import  obtener_datos_empresas;
from enterprises.views import  predecirValor;
from enterprises.views import test_mongo_connection, obtener_predicciones_email, guardar_prediccion



#se elimino esta ruta, ya que esta se hace desde apps.py al encender el servidor
#path('cargar_datos_todas_empresas', cargar_datos_empresas, name='cargar_datos_empresas'),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtener_datos_empresas', obtener_datos_empresas, name='obtener_datos_empresas'),
    path('obtener_datos_empresa/<str:nombre_empresa>/', obtener_datos_empresa, name='obtener_datos_empresa'),
    path('predecirValor/<str:ticker>/', predecirValor, name='predecirValor'),

    path('test-mongo-connection/', test_mongo_connection, name='test_mongo_connection'),
    path('guardar_prediccion/', guardar_prediccion, name='guardar_prediccion'),
    path('obtener_predicciones_email/<str:email>/', obtener_predicciones_email, name='obtener_predicciones_email'),
]

