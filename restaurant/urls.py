from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("review_create/", views.ReviewCreateView.as_view(), name="review-create"),
    path("about/", views.AboutView.as_view(), name="about"),
]