from django.urls import path
from django.http import HttpResponse

from Pokedex_selfee.Auth.views import LoginView


def hello_world(request):
    return HttpResponse("Hello World !")

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('login/', LoginView.as_view(), name='login'),
    path('session/', LoginView.as_view(), name='session_status'),
    path('logout/', LoginView.as_view(), name='logout'),
    path('update/', LoginView.as_view(), name='update_user'),
]