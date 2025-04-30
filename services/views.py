from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import MealCategoryForm, MealForm
from .models import Meal, MealCategory


class BanquetView(TemplateView):
    template_name = "services/banquet.html"


class MenuView(ListView):
    model = MealCategory
    template_name = "services/menu.html"
    context_object_name = "categories"


class MenuDetailView(ListView):
    model = Meal
    template_name = "services/menu_detail.html"
    context_object_name = "meals"

    def get_queryset(self):
        return Meal.objects.filter(category=self.kwargs["pk"])


class DeliveryView(TemplateView):
    template_name = "services/delivery.html"


class TourView(TemplateView):
    template_name = "services/tour.html"


class MealListView(ListView):
    model = Meal
    template_name = "services/admin/meal_list.html"
    context_object_name = "meals"

    def get_queryset(self):
        return Meal.objects.filter(category=self.kwargs["pk"])


class MealCreateView(CreateView):
    model = Meal
    template_name = "services/admin/meal_form.html"
    form_class = MealForm

    def get_success_url(self):
        return reverse_lazy("services:meal-list", kwargs={"pk": self.object.category.pk})


class MealUpdateView(UpdateView):
    model = Meal
    template_name = "services/admin/meal_form.html"
    form_class = MealForm

    def get_success_url(self):
        return reverse_lazy("services:meal-list", kwargs={"pk": self.object.category.pk})


class MealDeleteView(DeleteView):
    model = Meal
    template_name = "services/admin/meal_delete.html"
    success_url = reverse_lazy("services:meal-list")


class MealCategoryListView(ListView):
    model = MealCategory
    template_name = "services/admin/meal_category_list.html"
    context_object_name = "categories"


class MealCategoryCreateView(CreateView):
    model = MealCategory
    form_class = MealCategoryForm
    template_name = "services/admin/meal_category_form.html"
    success_url = reverse_lazy("services:meal-category-list")


class MealCategoryUpdateView(UpdateView):
    model = MealCategory
    form_class = MealCategoryForm
    template_name = "services/admin/meal_category_form.html"
    success_url = reverse_lazy("services:meal-category-list")


class MealCategoryDeleteView(DeleteView):
    model = MealCategory
    template_name = "services/admin/meal_category_delete.html"
    success_url = reverse_lazy("services:meal-category-list")
    context_object_name = "category"
