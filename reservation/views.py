from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView

from .forms import ReservationStep1Form, ReservationStep2Form
from .models import Reservation, Table


class ReservationAdminListView(ListView):
    model = Reservation
    template_name = "reservation/admin/reservation_list.html"
    context_object_name = "reservations"


class ReservationAdminDeleteView(DeleteView):
    model = Reservation
    template_name = "reservation/admin/reservation_delete.html"
    success_url = reverse_lazy("restaurant:reservation-list")


class ReservationStep1View(FormView):
    template_name = "reservation/reservation1_form.html"
    form_class = ReservationStep1Form
    success_url = reverse_lazy("reservation:reservation-step2")

    def form_valid(self, form):
        # Convert date and time objects to strings before saving in the session
        cleaned_data = form.cleaned_data
        cleaned_data["date"] = cleaned_data["date"].isoformat()
        cleaned_data["start_time"] = cleaned_data["start_time"].isoformat()
        cleaned_data["end_time"] = cleaned_data["end_time"].isoformat()
        self.request.session["reservation_step1_data"] = cleaned_data
        return super().form_valid(form)


class ReservationStep2View(FormView):
    template_name = "reservation/reservation2_form.html"
    form_class = ReservationStep2Form
    success_url = reverse_lazy("restaurant:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Retrieve step 1 data from the session
        step1_data = self.request.session.get("reservation_step1_data")
        if not step1_data:
            return HttpResponseRedirect(reverse_lazy("reservation:reservation-step1"))

        # Filter available tables based on step 1 data
        date = step1_data["date"]
        start_time = step1_data["start_time"]
        end_time = step1_data["end_time"]
        total_persons = step1_data["total_persons"]

        reserved_tables = Reservation.objects.filter(
            date=date, start_time__lt=end_time, end_time__gt=start_time
        ).values_list("table_id", flat=True)

        available_tables = Table.objects.exclude(id__in=reserved_tables).filter(capacity__gte=total_persons)
        kwargs["available_tables"] = available_tables

        # Pass step 1 data to the form for validation
        kwargs["initial"] = {
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
        }
        return kwargs

    def form_valid(self, form):
        # Retrieve step 1 data from the session
        step1_data = self.request.session.get("reservation_step1_data")
        if not step1_data:
            return HttpResponseRedirect(reverse_lazy("reservation:reservation-step1"))

        # Save the reservation
        table = form.cleaned_data["table"]
        if self.request.user.groups.filter(name="Manager").exists():
            customer = None
        else:
            customer = self.request.user
        Reservation.objects.create(
            table=table,
            date=step1_data["date"],
            start_time=step1_data["start_time"],
            end_time=step1_data["end_time"],
            total_persons=step1_data["total_persons"],
            user=customer,
        )

        # Mark the table as reserved
        table.is_reserved = True
        table.save()

        # Clear session data after successful reservation
        del self.request.session["reservation_step1_data"]

        return super().form_valid(form)