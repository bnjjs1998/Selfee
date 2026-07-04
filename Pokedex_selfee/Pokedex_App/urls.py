from django.urls import path
from django.http import HttpResponse
from .service import get_pokemon_data
from .views import get_pokemon_view


def hello_world(request):
    return HttpResponse("Hello World !")



urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('pokemon/<str:pokemon_name>/', get_pokemon_view, name='get_pokemon_data'),
]
