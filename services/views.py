from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import MealCategoryForm, MealForm
from .models import Meal, MealCategory
from .services import MealCategoryService, MealService

CACHE_TIMEOUT = settings.CACHE_TIMEOUT if settings.CACHE_ENABLED else 0


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class BanquetView(TemplateView):
    template_name = "services/banquet.html"


class MenuView(ListView):
    model = MealCategory
    template_name = "services/menu.html"
    context_object_name = "categories"

    def get_queryset(self):
        return MealCategoryService.get_all_categories()


class MenuDetailView(ListView):
    model = Meal
    template_name = "services/menu_detail.html"
    context_object_name = "meals"

    def get_queryset(self):
        return MealService.get_all_meals_in_category(category=self.kwargs["pk"])


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class DeliveryView(TemplateView):
    template_name = "services/delivery.html"


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class TourView(TemplateView):
    template_name = "services/tour.html"


class MealListView(PermissionRequiredMixin, ListView):
    model = Meal
    template_name = "services/admin/meal_list.html"
    context_object_name = "meals"
    permission_required = "services.can_admin_website"

    def get_queryset(self):
        return MealService.get_all_meals_in_category(category=self.kwargs["pk"])


class MealCreateView(PermissionRequiredMixin, CreateView):
    model = Meal
    template_name = "services/admin/meal_form.html"
    form_class = MealForm
    permission_required = "services.can_admin_website"

    def get_success_url(self):
        return reverse_lazy("services:meal-list", kwargs={"pk": self.object.category.pk})


class MealUpdateView(PermissionRequiredMixin, UpdateView):
    model = Meal
    template_name = "services/admin/meal_form.html"
    form_class = MealForm
    permission_required = "services.can_admin_website"

    def get_success_url(self):
        return reverse_lazy("services:meal-list", kwargs={"pk": self.object.category.pk})


class MealDeleteView(PermissionRequiredMixin, DeleteView):
    model = Meal
    template_name = "services/admin/meal_delete.html"
    permission_required = "services.can_admin_website"

    def get_success_url(self):
        return reverse_lazy("services:meal-list", kwargs={"pk": self.object.category.pk})


class MealCategoryListView(PermissionRequiredMixin, ListView):
    model = MealCategory
    template_name = "services/admin/meal_category_list.html"
    context_object_name = "categories"
    permission_required = "services.can_admin_website"

    def get_queryset(self):
        return MealCategoryService.get_all_categories()


class MealCategoryCreateView(PermissionRequiredMixin, CreateView):
    model = MealCategory
    form_class = MealCategoryForm
    template_name = "services/admin/meal_category_form.html"
    success_url = reverse_lazy("services:meal-category-list")
    permission_required = "services.can_admin_website"


class MealCategoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = MealCategory
    form_class = MealCategoryForm
    template_name = "services/admin/meal_category_form.html"
    success_url = reverse_lazy("services:meal-category-list")
    permission_required = "services.can_admin_website"


class MealCategoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = MealCategory
    template_name = "services/admin/meal_category_delete.html"
    success_url = reverse_lazy("services:meal-category-list")
    context_object_name = "category"
    permission_required = "services.can_admin_website"
