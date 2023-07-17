from django.urls import path
from .views import LoginView, HomeView, DetectionView, SignupView

app_name = "website"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(),name='register'),
    path('home/', HomeView.as_view(), name='home'),
    path('detection/', DetectionView.as_view())
]