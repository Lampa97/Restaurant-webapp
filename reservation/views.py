from django.shortcuts import render
from django.views.generic import CreateView
from .forms import ReservationForm
from .models import Table, Reservation


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation/reservation_form.html"
    success_url = "restaurant:home"  # Redirect to a success page after successful submission

    def form_valid(self, form):
        # Mark the selected table as reserved
        table = form.cleaned_data['table']
        table.is_reserved = True
        table.save()

        reservation = form.save(commit=False)
        reservation.customer = self.request.user
        reservation.save()

        # Update the user status
        user = self.request.user
        user.had_booked = True
        user.save()

        # You can add any additional processing here if needed
        return super().form_valid(form)
