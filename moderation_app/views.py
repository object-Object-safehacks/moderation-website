from django.shortcuts import render, redirect
from django.http import HttpResponse
import discordoauth2
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Guild, UserGuild, Message, Attachment, Turnstile
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from turnstile.fields import TurnstileField
from django import forms
from django.http import JsonResponse

class turnstileForm(forms.Form):
    turnstile = TurnstileField(theme='dark', size='compact')

class actionForm(forms.Form):
    message_id = forms.IntegerField()
    action = forms.CharField(max_length=999)

base_url = settings.BASE_URL
endpoint_url = base_url + "/oauth2"

api_url = settings.API_URL

client = discordoauth2.Client(1249086752497598534, secret="wCaVKNOQCzcmrX-b5mW_2YI5rJMBP75r", redirect=endpoint_url)

def index(request):
    return render(request, "moderation_app/index.html")

def manage(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(client.generate_uri(scope=["identify",  "guilds"]))

    userGuildObj = UserGuild.objects.get(user=user)

    data = {
        "guilds": []
    }

    for guild in userGuildObj.guilds.all():
        data['guilds'].append({"name": guild.name, "id": guild.id})
    
    print(data)
    
    return render(request, 'moderation_app/manage.html', data)

def messages(request, guild_id):
    guildobj = Guild.objects.get(id=guild_id)

    if request.method == "POST":
        form = actionForm(request.POST)
        if form.is_valid():
            message_id = form.cleaned_data["message_id"]
            action = form.cleaned_data["action"]
            message_obj = Message.objects.get(id=message_id)
            if action == "unflag":
                Message.objects.filter(id=message_id).delete()
            userId = message_obj.userId
            jsonObj = {
                'guild': str(guild_id),
                'user': str(userId),
                'time': 300000,
                'message': str(message_id)
            }

            url = api_url + "actions/" + action

            r = requests.post(url, json = jsonObj)

            print(f"sending post data: {jsonObj} to {url}")
    
    messagesObjs = Message.objects.all().filter(guild=guildobj)

    print(f"messagesObjs {messagesObjs}")

    data = {
        "messages": messagesObjs,
        "guild_name": guildobj.name
    }

    return render(request, 'moderation_app/messages.html', data)

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

def turnstile(request, turnstile_id):
    print(turnstile_id)

    turnstile_obj = Turnstile.objects.get(id=turnstile_id)

    if request.method == "POST":
        form = turnstileForm(request.POST)

        if form.is_valid():
            turnstile_obj.isCompleted = True
            turnstile_obj.save()
            return HttpResponse("Verification Complete!")
        else:
            return HttpResponse("Could not verify, please try again")

    if turnstile_obj.isCompleted == True:
        return HttpResponse("Verification Complete!")

    form = turnstileForm()

    return render(request, "moderation_app/turnstile.html", {"form": form})

# API

@csrf_exempt
def report(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user = body["user"]
        channel = body["channel"]
        message = body["message"]
        messageObj = Message(
            username = user["name"],
            userId = user["id"],
            channel = channel["id"],
            channelName = channel["name"],
            messageId = message["id"],
            content = message["content"],
            time = body["time"],
            reason = body["reason"]
        )

        turnstileObj = Turnstile()
        turnstileObj.save()

        returnJson = {
            "url": f"{base_url}/turnstile/{turnstileObj.id}",
            "id": turnstileObj.id,
        }

        messageObj.turnstile = turnstileObj

        messageObj.save()
        messageObj.guild.add(Guild.objects.get(id=int(body["guild"])))

        for attachment in message["attachments"]:
            attachmentObj = Attachment(url=attachment)
            attachmentObj.save()
            messageObj.attachments.add(attachmentObj)

        messageObj.save()

        return JsonResponse(returnJson)
    else:
        return HttpResponse("GET is cringe, use POST")

@csrf_exempt
def getTurnstileStatus(request, turnstile_id):
    turnstile_obj = Turnstile.objects.get(id=turnstile_id)

    return JsonResponse(
        {"completed": turnstile_obj.isCompleted}
    )
