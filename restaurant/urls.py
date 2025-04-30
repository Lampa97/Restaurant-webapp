from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("restaurant/admin/review/", views.ReviewListView.as_view(), name="review-list"),
    path("review/create/", views.ReviewCreateView.as_view(), name="review-create"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("restaurant/admin/personnel/", views.PersonnelListView.as_view(), name="personnel-list"),
    path("restaurant/admin/personnel/create/", views.PersonnelCreateView.as_view(), name="personnel-create"),
    path("restaurant/admin/personnel/<int:pk>/update/", views.PersonnelUpdateView.as_view(), name="personnel-update"),
    path("restaurant/admin/personnel/<int:pk>/delete/", views.PersonnelDeleteView.as_view(), name="personnel-delete"),
    path("restaurant/admin/service/", views.ServiceListView.as_view(), name="service-list"),
    path("restaurant/admin/service/create/", views.ServiceCreateView.as_view(), name="service-create"),
    path("restaurant/admin/service/<int:pk>/update/", views.ServiceUpdateView.as_view(), name="service-update"),
    path("restaurant/admin/service/<int:pk>/delete/", views.ServiceDeleteView.as_view(), name="service-delete"),


]
