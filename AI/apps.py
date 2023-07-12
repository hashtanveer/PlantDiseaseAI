from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AI'

    def ready(self):
        import AI.signals
