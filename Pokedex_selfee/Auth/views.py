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


class SessionView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Utilisateur non authentifi d,mkdqsldkddmkslkdksS'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_groups = list(request.user.groups.values_list('name', flat=True))
        
        return Response({
            'authenticated': request.user.is_authenticated,
            'user_id': request.user.pk if request.user.is_authenticated else None,
            'username': request.user.username if request.user.is_authenticated else None,
            'user_groups': user_groups,
            'message': 'Session valide',
        })


class LogoutView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _logout_response(self, request):
        logout(request)
        response = Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SESSION_COOKIE_NAME)
        return response

    def post(self, request):
        return self._logout_response(request)

    def delete(self, request):
        return self._logout_response(request)
    


class UserGroupView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_groups = list(request.user.groups.values_list('name', flat=True))
        return Response({'user_groups': user_groups}, status=status.HTTP_200_OK)