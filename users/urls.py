from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, MeView, ForgotPasswordView, VerifyResetCodeView, ResetPasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', MeView.as_view(), name='me'),
    path("forgot-password/", ForgotPasswordView.as_view(), name='forgot-password'),
    path("verify-reset/", VerifyResetCodeView.as_view(), name='verify-reset-code'),
    path("reset-password/", ResetPasswordView.as_view(), name='reset-password'),
]




