from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.getContent, name="getContent"),
    path("wikiSearch/", views.wikiSearch, name="wikiSearch"),
    path("newPage/", views.newPage, name="newPage"),
    path("newEntry/", views.newEntry, name="newEntry"),
    path("editPage/<str:title>", views.editPage, name="editPage"),
    path("writeEdit/<str:title>", views.writeEdit, name="writeEdit"),
    path("randomPage/", views.randomPage, name="randomPage")
]
