# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer
from rest_framework import generics, permissions, exceptions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_password(request):
    newPassword = request.data.get('newPassword', None)
    user = request.user

    if not newPassword:
        raise exceptions.APIException({'newPassword': 'newPassword cannot be empty'})

    user.set_password(newPassword)
    user.save()

    
    Token.objects.get(user=user).delete()
    

    token = Token.objects.create(user=user)

    return Response({"message": "Password updated successfully", "token": token.key})


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user 

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def perform_create(self, serializer):
        password = self.request.data.get('password')
        user = serializer.save()
        user.set_password(password)
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user_details = UserSerializer(user).data
        token = serializer.validated_data

        return Response({
            'token': token['access'],
            'userdetails': user_details
        })


