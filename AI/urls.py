from django.urls import path
from .views import DiseaseDetectionCreationView, DetectionInformation, ListDetectionsForUser, ListDetectionModels

urlpatterns = [
    path('create', DiseaseDetectionCreationView.as_view()),
    path('info', DetectionInformation.as_view()),
    path('list', ListDetectionsForUser.as_view()),
    path('models', ListDetectionModels.as_view())
]