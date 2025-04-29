from django.urls import path

from . import views

app_name = "services"

urlpatterns = [
    path("banquet/", views.BanquetView.as_view(), name="banquet"),
    path("tour/", views.TourView.as_view(), name="tour"),
    path("delivery/", views.DeliveryView.as_view(), name="delivery"),
    path("menu/", views.MenuView.as_view(), name="menu"),
    path("menu/<int:pk>/", views.MenuDetailView.as_view(), name="menu-detail"),
    path("admin/menu/meal/<int:pk>/", views.MealListView.as_view(), name="meal-list"),
    path("admin/menu/meal/create/", views.MealCreateView.as_view(), name="meal-create"),
    path("admin/menu/meal/<int:pk>/update/", views.MealUpdateView.as_view(), name="meal-update"),
    path("admin/menu/meal/<int:pk>/delete/", views.MealDeleteView.as_view(), name="meal-delete"),
    path("admin/menu/", views.MealCategoryListView.as_view(), name="meal-category-list"),
    path("admin/menu/create/", views.MealCategoryCreateView.as_view(), name="meal-category-create"),
    path("admin/menu/<int:pk>/update/", views.MealCategoryUpdateView.as_view(), name="meal-category-update"),
    path("admin/menu/<int:pk>/delete/", views.MealCategoryDeleteView.as_view(), name="meal-category-delete"),

]
