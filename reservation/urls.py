from django.urls import path

from . import views

app_name = "reservation"

urlpatterns = [
    path("reservation_create/", views.ReservationCreateView.as_view(), name="reservation-create"),
]
