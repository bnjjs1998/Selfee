from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service import get_pokemon_list_by_types_service


class PokemonListView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_group_names = list(request.user.groups.values_list('name', flat=True))
        pokemon_list = get_pokemon_list_by_types_service(user_group_names)

        if isinstance(pokemon_list, dict) and 'error' in pokemon_list:
            return Response(pokemon_list, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({'pokemons': pokemon_list}, status=status.HTTP_200_OK)
