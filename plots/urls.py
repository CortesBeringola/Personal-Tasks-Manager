from django.urls import path

from . import views

urlpatterns = [
    path("plotting/", views.finance, name="finance"),
    path("api", views.ChartData.as_view(), name="finance"),
    path("reports/<int:report_user>/<int:report_year>/<int:report_month>/<int:report_day>/<int:report_hour>/"
         "<int:report_minute>", views.GeneratePdf.as_view(), name="reports"),
]
