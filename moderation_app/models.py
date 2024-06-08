from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Guild(models.Model):
    name = models.CharField(max_length=999)

class UserGuild(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guilds = models.ManyToManyField("Guild", blank=True)
