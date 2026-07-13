from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token



class UserGroupView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_groups = list(request.user.groups.values_list('name', flat=True))
        return Response(
            {
                'user_id': request.user.pk,
                'username': request.user.username,
                'user_groups': user_groups,
            },
            status=status.HTTP_200_OK,
        )