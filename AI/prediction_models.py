
class PredictionModelsManager:
    _prediction_models = {}

    @property
    def prediction_models(self):
        return self._prediction_models

    def update_prediction_models(self):
        from .utils import load_prediction_models
        self._prediction_models = load_prediction_models()

prediction_models_manager = PredictionModelsManager()
