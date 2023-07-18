from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    def get(self, request, format=None):
        return render(request, 'user/signin.html')

class SignupView(APIView):
    def get(self, request, format=None):
        return render(request, 'user/signup.html')
    

class HomeView(APIView): 
    def get(self, request, format=None):
        return render(request,'website/index.html')
    
class DetectionView(APIView):
    def get(self, request, format=None):
        return render(request,'website/detection.html')

class AboutView(APIView):
    def get(self, request, format=None):
        return render(request,'website/about.html')