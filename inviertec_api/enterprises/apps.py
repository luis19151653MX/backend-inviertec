from django.apps import AppConfig

class EnterprisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'enterprises'

    def ready(self):
        print("Ejecutando inviertec")
        # Importa y ejecuta la función cargar_datos_empresas
        from enterprises.views import cargar_datos_empresas
        cargar_datos_empresas()
        