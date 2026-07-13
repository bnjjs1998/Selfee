from django.urls import path
from django.http import HttpResponse
from Pokedex_selfee.Auth.Views.Login_views import LoginView
from Pokedex_selfee.Auth.Views.Logout_views import LogoutView
from Pokedex_selfee.Auth.Views.sessions_views import SessionView
from Pokedex_selfee.Auth.Views.UserGroup_Views import UserGroupView


def hello_world(request):
    return HttpResponse("Hello World !")

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('login/', LoginView.as_view(), name='login'),
    path('session/', SessionView.as_view(), name='session_status'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/me/', UserGroupView.as_view(), name='user_me'),
]