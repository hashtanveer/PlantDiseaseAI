from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class LoginView(APIView):
    def get(self, request, format=None):
        return render(request, 'user/login.html')
    

class HomeView(APIView):
    def get(self, request, format=None):
        return render(request,'website/index.html')