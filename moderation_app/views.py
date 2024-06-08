from django.shortcuts import render, redirect
from django.http import HttpResponse
import discordoauth2
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Guild, UserGuild
import requests


base_url = settings.BASE_URL
endpoint_url = base_url + "/oauth2"

api_url = settings.API_URL

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
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("failed to login")
    return redirect("/manage")

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

        guild_list = []

        for guild in guilds:
            guild_id = guild['id']
            guild_name = guild['name']

            # check if user is admin in guild
            url = api_url + "user"
            jsonObj = {
                'id': str(user.id),
                'guild': str(guild_id)
            }

            print(f"what im sending to server {jsonObj}")
            
            r = requests.post(url, json = jsonObj)

            print(f"json {r.json()}")

            json_return = r.json()
            try:
                hasPermission = json_return['hasPermission']
            except:
                hasPermission = False

            if hasPermission:
                try:
                    guild_obj = Guild.objects.get(id=guild_id)
                except Guild.DoesNotExist:
                    print(f"guild {guild_name} does not exist, creating one")
                    guild_obj = Guild(id=guild_id, name=guild_name)
                    guild_obj.save()
                guild_list.append(guild_id)
        
        # update guilds for user
        try:
            user_guild = UserGuild.objects.get(user=user)
        except UserGuild.DoesNotExist:
            print("userguild does not exist, creating one")
            user_guild = UserGuild(user=user)
            user_guild.save()

        print(f"guild list {guild_list}")

        for guild_list_id in guild_list:
            guild = Guild.objects.get(id=guild_list_id)
            print(f"adding guild {guild}")
            user_guild.guilds.add(guild)
        
        user_guild.save()

        
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def log_out(request):
    logout(request)
    return redirect("/")
