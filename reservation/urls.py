from django.urls import path

from . import views

app_name = "reservation"

urlpatterns = [
    path("create/step1/", views.ReservationStep1View.as_view(), name="reservation-step1"),
    path("create/step2/", views.ReservationStep2View.as_view(), name="reservation-step2"),
    path("update/<int:pk>/step1/", views.ReservationAdminStep1UpdateView.as_view(), name="reservation-update-step1"),
    path("admin/list/", views.ReservationAdminListView.as_view(), name="reservation-list"),
    path("admin/<int:pk>/delete/", views.ReservationAdminDeleteView.as_view(), name="reservation-delete"),
    path("admin/table/", views.TableListView.as_view(), name="table-list"),
    path("admin/table/create/", views.TableCreateView.as_view(), name="table-create"),
    path("admin/table/<int:pk>/update/", views.TableUpdateView.as_view(), name="table-update"),
    path("admin/table/<int:pk>/delete/", views.TableDeleteView.as_view(), name="table-delete"),
]
