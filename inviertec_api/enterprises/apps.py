from django.apps import AppConfig

class EnterprisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enterprises'

    def ready(self):
        # Importa y ejecuta la función cargar_datos_empresas
        from enterprises.views import cargar_datos_empresas
        print("Ejecutando inviertec")
        cargar_datos_empresas()
        print("Datos cargados")
        