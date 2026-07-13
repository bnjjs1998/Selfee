from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'authenticated': request.user.is_authenticated,
            'user_id': request.user.pk if request.user.is_authenticated else None,
        })

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Connecté avec succès',
                'user_id': user.pk,
                'token': token.key,
            })

        return Response({'error': 'Identifiants invalides'}, status=status.HTTP_400_BAD_REQUEST)

