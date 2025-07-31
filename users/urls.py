from django.urls import path
from .views import (
    SendOTPView, VerifyOTPView, RegisterView, UserDetailView, UserUpdateView,
    ConfirmDeletionView, PreDeletionView, DeleteUserView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('confirm-deletion/', ConfirmDeletionView.as_view()),
    path('pre-deletion/', PreDeletionView.as_view()),
    path('delete/', DeleteUserView.as_view()),
    path('detail/', UserDetailView.as_view()),
    path('update/', UserUpdateView.as_view()),
]
