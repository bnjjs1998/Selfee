
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from ..service.types_service import add_pokemon_type_service


@require_POST
def add_pokemon_type_view(request, pokemon_type):
    """Handle adding/fetching data for a given pokemon type.

    Expects `pokemon_type` from the URL and returns JSON from the service.
    """
    result = add_pokemon_type_service(pokemon_type)
    status = 200 if "error" not in result else 404
    return JsonResponse(result, status=status)


# DRF-based view to remove a type from the authenticated user's groups
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.models import Group


class UserGroupRemoveView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pokemon_type):
        try:
            grp = Group.objects.get(name__iexact=pokemon_type)
        except Group.DoesNotExist:
            return Response({'error': 'Groupe introuvable'}, status=drf_status.HTTP_404_NOT_FOUND)

        if not request.user.groups.filter(pk=grp.pk).exists():
            return Response({'error': "L'utilisateur n'appartient pas à ce groupe"}, status=drf_status.HTTP_400_BAD_REQUEST)

        request.user.groups.remove(grp)
        return Response({'message': f"Groupe '{grp.name}' supprimé de l'utilisateur"}, status=drf_status.HTTP_200_OK)