from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .group_type_validation import is_valid_pokemon_type


class UserGroupRemoveView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _remove_group(self, request, pokemon_type):
        is_valid_type = is_valid_pokemon_type(pokemon_type)
        if is_valid_type is None:
            return Response(
                {"error": "Impossible de valider le type Pokemon pour le moment"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if not is_valid_type:
            return Response({"error": "Type de Pokemon introuvable"}, status=status.HTTP_404_NOT_FOUND)

        normalized_type = pokemon_type.lower()
        try:
            group = Group.objects.get(name=normalized_type)
        except Group.DoesNotExist:
            return Response({"error": "Groupe introuvable"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.groups.filter(pk=group.pk).exists():
            return Response({"error": "L'utilisateur n'appartient pas a ce groupe"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.groups.remove(group)
        return Response(
            {"message": f"Groupe '{group.name}' supprime de l'utilisateur"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, pokemon_type):
        return self._remove_group(request, pokemon_type)

    def delete(self, request, pokemon_type):
        return self._remove_group(request, pokemon_type)
