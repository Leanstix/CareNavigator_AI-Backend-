from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserDetailView, ProviderListView, AppointmentView, RegisterView, LogoutView

urlpatterns = [
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('providers/', ProviderListView.as_view(), name='provider-list'),
    path('appointments/', AppointmentView.as_view(), name='appointment-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
