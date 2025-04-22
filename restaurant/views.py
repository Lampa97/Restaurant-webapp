from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import ReviewForm
from .models import Review, Personnel, Service


class HomeView(TemplateView):
    template_name = "restaurant/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'restaurant:review_form'
    success_url = 'restaurant:home'  # Redirect to the home page after successful submission

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)




