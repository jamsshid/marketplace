from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import RegisterView, ProfileView, UnifiedLoginView, LogoutView, UserDashboardView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", UnifiedLoginView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ProfileView.as_view(), name="user_profile"),
    path("dashboard/", UserDashboardView.as_view(), name="dashboard"),
]
