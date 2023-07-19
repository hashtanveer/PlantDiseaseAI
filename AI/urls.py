from django.urls import path
from .views import DiseaseDetectionCreationView, DetectionInformation, ListDetectionsForUser, ListDetectionModels

app_name = 'AI'

urlpatterns = [
    path('create', DiseaseDetectionCreationView.as_view(), name='create'),
    path('info', DetectionInformation.as_view()),
    path('list', ListDetectionsForUser.as_view()),
    path('models', ListDetectionModels.as_view(), name='models')
]