from django.urls import path

from . import views

app_name = "reservation"

urlpatterns = [
    path("create/step1/", views.ReservationStep1View.as_view(), name="reservation-step1"),
    path("create/step2/", views.ReservationStep2View.as_view(), name="reservation-step2"),
    path("admin/list/", views.ReservationAdminListView.as_view(), name="reservation-list"),
    path("admin/delete/<int:pk>/", views.ReservationAdminDeleteView.as_view(), name="reservation-delete"),
]
