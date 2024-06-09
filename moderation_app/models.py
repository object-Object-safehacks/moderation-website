from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Guild(models.Model):
    name = models.CharField(max_length=999)

class UserGuild(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guilds = models.ManyToManyField("Guild", blank=True)

class Message(models.Model):
    username = models.CharField(max_length=999)
    userId = models.BigIntegerField()
    guild = models.ManyToManyField("Guild", blank=True)
    channel = models.BigIntegerField()
    channelName = models.CharField(max_length=999)
    messageId = models.BigIntegerField()
    content = models.CharField(max_length=9999)
    attachments = models.ManyToManyField("Attachment", blank=True)
    reason = models.CharField(max_length=999)
    time = models.DateTimeField()
    turnstile = models.OneToOneField("Turnstile", on_delete=models.CASCADE, default=None)

class Attachment(models.Model):
    url = models.CharField(max_length=9999)

class Turnstile(models.Model):
    isCompleted = models.BooleanField(default=False)
