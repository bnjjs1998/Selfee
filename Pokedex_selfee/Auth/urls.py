from django.urls import path
from django.http import HttpResponse

from Pokedex_selfee.Auth.views import LoginView

# On définit une vue simple directement ici
def hello_world(request):
    return HttpResponse("Hello World !")

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('login/', LoginView.as_view(), name='login'),
]