from django.contrib import admin
from django.urls import path
from enterprises.views import obtener_datos_empresa;
#from enterprises.views import cargar_datos_empresas;
from enterprises.views import  obtener_datos_empresas;
from enterprises.views import  predecirValor;


#se elimino esta ruta, ya que esta se hace desde apps.py al encender el servidor
#path('cargar_datos_todas_empresas', cargar_datos_empresas, name='cargar_datos_empresas'),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtener_datos_empresas', obtener_datos_empresas, name='obtener_datos_empresas'),
    path('obtener_datos_empresa/<str:nombre_empresa>/', obtener_datos_empresa, name='obtener_datos_empresa'),
    path('predecirValor/<str:nombre_empresa>/', predecirValor, name='predecirValor'),
]

