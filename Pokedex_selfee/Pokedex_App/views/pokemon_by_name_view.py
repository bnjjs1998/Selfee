from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..service import get_pokemon_data
from .pokemon_List_Filtered import filter_pokemon_types_by_groups


class PokemonByNameView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pokemon_name):
        pokemon_data = get_pokemon_data(pokemon_name)
        if pokemon_data is None:
            return Response({'error': 'Pokemon non trouve'}, status=status.HTTP_404_NOT_FOUND)

        user_group_names = set(request.user.groups.values_list('name', flat=True))
        filtered_payload = filter_pokemon_types_by_groups(pokemon_data, user_group_names)

        # Strict access: user must share at least one Pokemon type via group membership.
        if not filtered_payload.get('types'):
            return Response({'error': 'Acces refuse a ce pokemon'}, status=status.HTTP_403_FORBIDDEN)

        return Response(filtered_payload, status=status.HTTP_200_OK)
