from django.urls import path

from . import views

urlpatterns = [
    path("plotting/", views.plotting, name="plotting"),
]
