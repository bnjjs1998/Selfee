from django.contrib.auth.models import Group
from rest_framework import status as drf_status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service.types_service import get_all_types_service


def _is_valid_pokemon_type(pokemon_type):
    response = get_all_types_service()
    if "error" in response:
        return None

    available_types = set(response.get("types", []))
    return pokemon_type.lower() in available_types


class UserGroupAddView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pokemon_type):
        is_valid_type = _is_valid_pokemon_type(pokemon_type)
        if is_valid_type is None:
            return Response(
                {"error": "Impossible de valider le type Pokemon pour le moment"},
                status=drf_status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if not is_valid_type:
            return Response({"error": "Type de Pokemon introuvable"}, status=drf_status.HTTP_404_NOT_FOUND)

        normalized_type = pokemon_type.lower()
        group, _ = Group.objects.get_or_create(name=normalized_type)
        request.user.groups.add(group)

        return Response(
            {
                "type": normalized_type,
                "message": "Ajout au groupe reussi",
            },
            status=drf_status.HTTP_200_OK,
        )


class UserGroupRemoveView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _remove_group(self, request, pokemon_type):
        is_valid_type = _is_valid_pokemon_type(pokemon_type)
        if is_valid_type is None:
            return Response(
                {"error": "Impossible de valider le type Pokemon pour le moment"},
                status=drf_status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        if not is_valid_type:
            return Response({"error": "Type de Pokemon introuvable"}, status=drf_status.HTTP_404_NOT_FOUND)

        normalized_type = pokemon_type.lower()
        try:
            grp = Group.objects.get(name=normalized_type)
        except Group.DoesNotExist:
            return Response({"error": "Groupe introuvable"}, status=drf_status.HTTP_404_NOT_FOUND)

        if not request.user.groups.filter(pk=grp.pk).exists():
            return Response({"error": "L'utilisateur n'appartient pas a ce groupe"}, status=drf_status.HTTP_400_BAD_REQUEST)

        request.user.groups.remove(grp)
        return Response({"message": f"Groupe '{grp.name}' supprime de l'utilisateur"}, status=drf_status.HTTP_200_OK)

    def post(self, request, pokemon_type):
        return self._remove_group(request, pokemon_type)

    def delete(self, request, pokemon_type):
        return self._remove_group(request, pokemon_type)