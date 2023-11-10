"""inviertec_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from enterprises.views import obtener_datos_empresa;
#from enterprises.views import cargar_datos_empresas;
from enterprises.views import  obtener_datos_empresas;


#se elimino esta ruta, ya que esta se hace desde apps.py al encender el servidor
#path('cargar_datos_todas_empresas', cargar_datos_empresas, name='cargar_datos_empresas'),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('obtener_datos_empresas', obtener_datos_empresas, name='obtener_datos_empresas'),
    path('obtener_datos_empresa/<str:nombre_empresa>/', obtener_datos_empresa, name='obtener_datos_empresa'),
]
