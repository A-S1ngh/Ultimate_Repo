from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("addpage/", views.addpage, name="addpage"),
    path("random/", views.randompage, name="random"),
    path("search/", views.search, name = "search"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("submitedit/<str:title>", views.submitedit, name="submitedit"),

]
