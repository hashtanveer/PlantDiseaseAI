from django.apps import AppConfig
from .prediction_models import prediction_models_manager

class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AI'

    def ready(self):
        import AI.signals
        prediction_models_manager.update_prediction_models()

