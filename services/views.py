from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView

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
