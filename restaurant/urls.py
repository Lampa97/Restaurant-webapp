from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
]