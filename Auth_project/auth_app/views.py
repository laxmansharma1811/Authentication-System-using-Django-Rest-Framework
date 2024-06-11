from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.data['email']
                password = serializer.data['password']

                user = authenticate(email=email, password=password)
                if user is None:
                    return Response({"message": "Invalid Credentials", "status": status.HTTP_400_BAD_REQUEST})
                
                refresh = RefreshToken.for_user(user)
                value = Response({"refresh": str(refresh), 
                                "access": str(refresh.access_token), 
                                "status": status.HTTP_200_OK})
                
                value.set_cookie(key='access', value=str(refresh.access_token), httponly=True)
                return value
            
            return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})
        
        except Exception as e:
            return Response({"message": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR})
        



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Registered Successfully", "status": status.HTTP_201_CREATED})
        
        return Response({"message": "Invalid data", "status": status.HTTP_400_BAD_REQUEST})




class LogoutView(APIView):
    def get(self, request):
        value = Response({"message": "Logged out successfully", "status": status.HTTP_200_OK})
        value.delete_cookie('access')
        return value
