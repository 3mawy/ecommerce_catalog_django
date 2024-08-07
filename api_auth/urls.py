from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api_auth.views import UserRegistrationView, CustomTokenObtainPairView, UserProfileView

urlpatterns = [
    path('profile', UserProfileView.as_view(), name='user-profile'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
]
