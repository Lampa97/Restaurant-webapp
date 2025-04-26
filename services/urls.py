from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("banquet/", views.BanquetView.as_view(), name="banquet"),
    path("tour/", views.TourView.as_view(), name="tour"),
    path("delivery/", views.DeliveryView.as_view(), name="delivery"),
    path("menu/", views.MenuView.as_view(), name="menu"),
    path("menu/<int:pk>/", views.MenuDetailView.as_view(), name="menu-detail"),
]