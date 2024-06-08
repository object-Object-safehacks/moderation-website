from django.shortcuts import render, redirect
from django.http import HttpResponse
import discordoauth2
from django.conf import settings
from django.contrib.auth.backends import BaseBackend


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
    print(request)
    return HttpResponse("oauth")

class SettingsBackend(BaseBackend):
    def authenticate(self, request, token):
        return
    """
        login_valid = settings.ADMIN_LOGIN == username
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None"""

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None