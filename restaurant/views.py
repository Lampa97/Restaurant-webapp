from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, UpdateView

from .forms import PersonnelForm, ReviewForm, ServiceForm
from .models import Personnel, Review, Service
from .services import count_avg_rating

CACHE_TIMEOUT = settings.CACHE_TIMEOUT if settings.CACHE_ENABLED else 0


class HomeView(TemplateView):
    template_name = "restaurant/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        context["services"] = Service.objects.all()
        return context


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class AboutView(TemplateView):
    template_name = "restaurant/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["personnel"] = Personnel.objects.all()
        return context


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class ServiceListView(PermissionRequiredMixin, ListView):
    model = Service
    template_name = "restaurant/admin/service_list.html"
    context_object_name = "services"
    permission_required = "restaurant.can_admin_website"


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "restaurant/admin/service_form.html"
    success_url = reverse_lazy("restaurant:service-list")
    permission_required = "restaurant.can_admin_website"


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "restaurant/admin/service_form.html"
    success_url = reverse_lazy("restaurant:service-list")
    permission_required = "restaurant.can_admin_website"


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    template_name = "restaurant/admin/service_delete.html"
    success_url = reverse_lazy("restaurant:service-list")
    permission_required = "restaurant.can_admin_website"


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class PersonnelListView(PermissionRequiredMixin, ListView):
    model = Personnel
    template_name = "restaurant/admin/personnel_list.html"
    context_object_name = "personnel"
    permission_required = "restaurant.can_admin_website"


class PersonnelCreateView(PermissionRequiredMixin, CreateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = "restaurant/admin/personnel_form.html"
    success_url = reverse_lazy("restaurant:personnel-list")
    permission_required = "restaurant.can_admin_website"


class PersonnelUpdateView(PermissionRequiredMixin, UpdateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = "restaurant/admin/personnel_form.html"
    success_url = reverse_lazy("restaurant:personnel-list")
    permission_required = "restaurant.can_admin_website"


class PersonnelDeleteView(PermissionRequiredMixin, DeleteView):
    model = Personnel
    template_name = "restaurant/admin/personnel_delete.html"
    success_url = reverse_lazy("restaurant:personnel-list")
    permission_required = "restaurant.can_admin_website"


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class ReviewListView(PermissionRequiredMixin, ListView):
    model = Review
    template_name = "restaurant/admin/review_list.html"
    context_object_name = "reviews"
    permission_required = "restaurant.can_admin_website"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avg_rating = count_avg_rating()
        context["avg_rating"] = avg_rating
        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "restaurant/home.html"
    success_url = reverse_lazy("restaurant:home")  # Redirect to the home page after successful submission
