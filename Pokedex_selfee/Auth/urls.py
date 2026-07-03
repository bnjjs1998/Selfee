from django.urls import path
from django.http import HttpResponse

# On définit une vue simple directement ici
def hello_world(request):
    return HttpResponse("Hello World !")

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
]