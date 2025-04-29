from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, DetailView, DeleteView

from .models import Meal, MealCategory


class BanquetView(TemplateView):
    template_name = "services/banquet.html"


class MenuView(ListView):
    model = Meal
    template_name = "services/menu.html"
    context_object_name = "meals"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = MealCategory.objects.all()
        return context


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
    template_name = "services/admin/meal_create.html"
    fields = ["name", "description", "price", "category", "image"]
    success_url = ""

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MealUpdateView(UpdateView):
    model = Meal
    template_name = "services/admin/meal_update.html"
    fields = ["name", "description", "price", "category", "image"]
    success_url = ""

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MealDeleteView(DeleteView):
    model = Meal
    template_name = "services/admin/meal_delete.html"
    success_url = ""


class MealCategoryListView(ListView):
    model = MealCategory
    template_name = "services/admin/meal_category_list.html"
    context_object_name = "meals"


class MealCategoryCreateView(CreateView):
    model = MealCategory
    template_name = "services/admin/meal_category_create.html"
    fields = ["name", "description", "image"]
    success_url = ""

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MealCategoryUpdateView(UpdateView):
    model = MealCategory
    template_name = "services/admin/meal_category_update.html"
    fields = ["name", "description", "image"]
    success_url = ""

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MealCategoryDeleteView(DeleteView):
    model = Meal
    template_name = "services/admin/meal_category_delete.html"
    success_url = ""
