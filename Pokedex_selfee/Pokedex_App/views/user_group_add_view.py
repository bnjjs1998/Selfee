from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .group_type_validation import is_valid_pokemon_type


class UserGroupAddView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        is_valid_type = is_valid_pokemon_type(pokemon_type)
        if is_valid_type is None:
            return Response(
                {"error": "Impossible de valider le type Pokemon pour le moment"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if not is_valid_type:
            return Response({"error": "Type de Pokemon introuvable"}, status=status.HTTP_404_NOT_FOUND)

        normalized_type = pokemon_type.lower()
        group, _ = Group.objects.get_or_create(name=normalized_type)
        request.user.groups.add(group)

        return Response(
            {
                "type": normalized_type,
                "message": "Ajout au groupe reussi",
            },
            status=status.HTTP_200_OK,
        )
