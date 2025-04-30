from django.urls import reverse_lazy
from .services import count_avg_rating
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView

from .forms import ReviewForm, ServiceForm, PersonnelForm
from .models import Personnel, Review, Service


class HomeView(TemplateView):
    template_name = "restaurant/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        context["services"] = Service.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "restaurant/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["personnel"] = Personnel.objects.all()
        return context


class ServiceListView(ListView):
    model = Service
    template_name = "restaurant/admin/service_list.html"
    context_object_name = "services"


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "restaurant/admin/service_form.html"
    success_url = reverse_lazy("restaurant:service-list")

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "restaurant/admin/service_form.html"
    success_url = reverse_lazy("restaurant:service-list")

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "restaurant/admin/service_delete.html"
    success_url = reverse_lazy("restaurant:service-list")


class PersonnelListView(ListView):
    model = Personnel
    template_name = "restaurant/admin/personnel_list.html"
    context_object_name = "personnel"


class PersonnelCreateView(CreateView):
    model =Personnel
    form_class = PersonnelForm
    template_name = "restaurant/admin/personnel_form.html"
    success_url = reverse_lazy("restaurant:personnel-list")


class PersonnelUpdateView(UpdateView):
    model = Personnel
    form_class = PersonnelForm
    template_name = "restaurant/admin/personnel_form.html"
    success_url = reverse_lazy("restaurant:personnel-list")


class PersonnelDeleteView(DeleteView):
    model = Personnel
    template_name = "restaurant/admin/personnel_delete.html"
    success_url = reverse_lazy("restaurant:personnel-list")


class ReviewListView(ListView):
    model = Review
    template_name = "restaurant/admin/review_list.html"
    context_object_name = "reviews"

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
