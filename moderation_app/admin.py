from django.contrib import admin
from .models import Guild, UserGuild, Message, Attachment

# Register your models here.
@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    pass

@admin.register(UserGuild)
class UserGuildAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass
