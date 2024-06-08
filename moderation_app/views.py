from django.shortcuts import render, redirect
from django.http import HttpResponse
import discordoauth2
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


base_url = settings.BASE_URL
endpoint_url = base_url + "/oauth2"

client = discordoauth2.Client(1249086752497598534, secret="wCaVKNOQCzcmrX-b5mW_2YI5rJMBP75r", redirect=endpoint_url)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def manage(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(client.generate_uri(scope=["identify",  "guilds"]))

    return HttpResponse(user.username)

def oauth2(request):
    oauth_code = request.GET['code']
    print(f"request {request.GET['code']}")

    user = authenticate(request, code=oauth_code)

    print(f"user {user}")

    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("failed to login")
    return HttpResponse("oauth")

class SettingsBackend(BaseBackend):
    def authenticate(self, request, code):
        try:
            access = client.exchange_code(code)
        except:
            return "false"
        print(f"access {access}")
        identify = access.fetch_identify()
        guilds = access.fetch_guilds()
        print(identify)
        print(guilds)
        id = identify['id']

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            # create new user
            print("user does not exist, creating one")
            user = User(id=id, username=identify['username'])
            user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None