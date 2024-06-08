from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("manage/", views.manage, name="manage"),
    path("oauth2/", views.oauth2, name="oauth2"),
    path("logout/", views.log_out, name="logout")
]