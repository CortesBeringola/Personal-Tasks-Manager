from django.urls import path

from . import views

urlpatterns = [
    path("plotting/", views.finance, name="finance"),
]
