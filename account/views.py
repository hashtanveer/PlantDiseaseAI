from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterationSerializer, LoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterationForm(APIView):
    def post(self, request, format=None):
        serializer = UserRegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response({"msg": "Registeration Sucessful",
                             "tokens": tokens},
                            status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginForm(APIView):
    def post(self, request, format=None):
        success = False
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"success": success,
                             "errors": serializer.errors
                            },
                            status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.data.get("email")
        password = serializer.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"success": success,
                             "errors":
                              {"non_field_errors":
                                ["Email or password doesn't match"]
                              }
                            },
                            status=status.HTTP_404_NOT_FOUND)
        success = True
        tokens = get_tokens_for_user(user)
        return Response({"sucess": success,
                         "tokens": tokens
                        },
                        status=status.HTTP_200_OK)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data,
                                                  context = {'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Reset password email sent'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data,
                                                 context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

