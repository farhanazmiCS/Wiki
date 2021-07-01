from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index),
    path("wiki/<str:entry>", views.entry, name="wiki"),
    path("createnewpage", views.create_page, name="create"),
    path("random", views.random_page, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("edit", views.index)
    ]
