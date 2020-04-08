from django.urls import path

from . import views

urlpatterns = [
    path("plotting/", views.finance, name="finance"),
    path("api", views.ChartData.as_view(), name="finance"),
]
