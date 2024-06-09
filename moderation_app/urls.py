from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("manage/", views.manage, name="manage"),
    path("messages/<int:guild_id>", views.messages, name="messages"),
    path("oauth2/", views.oauth2, name="oauth2"),
    path("logout/", views.log_out, name="logout"),
    path("turnstile/<int:turnstile_id>", views.turnstile),
    path("api/report", views.report, name="report"),
    path("api/getTurnstileStatus/<int:turnstile_id>", views.getTurnstileStatus),
]