from django.urls import path
from .views import LoginView, HomeView, DetectionView, SignupView, AboutView

app_name = "website"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(),name='register'),
    path('', HomeView.as_view(), name='home'),
    path('detection/', DetectionView.as_view(),name='detection'),
    path('about/', AboutView.as_view(), name='about'),
]