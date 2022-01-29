from django.urls import path

from . import views

app_name = "team_creator"
urlpatterns = [
    path("", views.index, name="index"),
]
