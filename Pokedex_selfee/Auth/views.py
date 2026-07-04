from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LoginView(APIView):
    permission_classes = ()

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
            return Response({
                'message': 'Connecté avec succès',
                'user_id': user.pk,
            })

        return Response({'error': 'Identifiants invalides'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)
    

    def put(self, request):
        return Response({'message': 'Mise à jour réussie'}, status=status.HTTP_200_OK)