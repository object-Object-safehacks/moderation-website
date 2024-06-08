from django.contrib import admin
from .models import Guild, UserGuild

# Register your models here.
@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    pass

@admin.register(UserGuild)
class UserGuildAdmin(admin.ModelAdmin):
    pass