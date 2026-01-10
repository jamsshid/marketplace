from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from django.contrib.auth import login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UnifiedLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            from django.contrib.auth import authenticate
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user) 

        return response

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Muvaffaqiyatli chiqildi (Logged out)."},
            status=status.HTTP_200_OK,
        )
