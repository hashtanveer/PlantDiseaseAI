from django.urls import path
from .views import LoginView, HomeView

app_name = "website"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), 
    path('home/', HomeView.as_view(), name='home')
]