from .views import UserRegisterationForm, UserLoginForm, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'account'

urlpatterns = [
    path('register/', UserRegisterationForm.as_view(), name='register'),
    path('signin/', UserLoginForm.as_view(), name='signin'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('forgotpassword/',SendPasswordResetEmailView.as_view(), name='forgotpassword' ),
    path('forgotpassword/<uid>/<token>', UserPasswordResetView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]