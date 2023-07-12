from .views import UserRegisterationForm, UserLoginForm, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterationForm.as_view()),
    path('signin/', UserLoginForm.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('forgotpassword/',SendPasswordResetEmailView.as_view(), name='forgotpassword' ),
    path('forgotpassword/<uid>/<token>', UserPasswordResetView.as_view()),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]