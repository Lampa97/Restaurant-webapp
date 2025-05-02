from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ReservationStep1Form, ReservationStep2Form, TableForm
from .models import Reservation, Table


class TableListView(PermissionRequiredMixin, ListView):
    model = Table
    template_name = "reservation/admin/table_list.html"
    context_object_name = "tables"
    permission_required = "reservation.can_admin_website"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tables = context["tables"]
        table_reservations = {
            table: table.reservations.all() for table in tables
        }
        context["table_reservations"] = table_reservations
        return context


class TableCreateView(PermissionRequiredMixin, CreateView):
    template_name = "reservation/admin/table_form.html"
    form_class = TableForm
    model = Table
    permission_required = "reservation.can_admin_website"
    success_url = reverse_lazy("reservation:table-list")


class TableUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = "reservation/admin/table_form.html"
    form_class = TableForm
    model = Table
    success_url = reverse_lazy("reservation:table-list")
    permission_required = "reservation.can_admin_website"


class TableDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = "reservation/admin/table_delete.html"
    permission_required = "reservation.can_admin_website"
    model = Table
    success_url = reverse_lazy("reservation:table-list")


class ReservationAdminListView(PermissionRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/admin/reservation_list.html"
    context_object_name = "reservations"
    permission_required = "reservation.can_admin_website"


class ReservationAdminStep1UpdateView(PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationStep1Form
    template_name = "reservation/admin/reservation1_form_update.html"
    permission_required = "reservation.can_admin_website"

    def form_valid(self, form):
        # Get the cleaned data
        cleaned_data = form.cleaned_data
        total_persons = cleaned_data.get("total_persons")
        table = self.object.table  # Get the table associated with the reservation

        # Check if total_persons exceeds the table capacity
        if total_persons > table.capacity:
            form.add_error("total_persons", f"Total persons cannot exceed the table capacity of {table.capacity}.")
            return self.form_invalid(form)

        # Convert date and time objects to strings before saving in the session
        cleaned_data["date"] = cleaned_data["date"].isoformat()
        cleaned_data["start_time"] = cleaned_data["start_time"].isoformat()
        cleaned_data["end_time"] = cleaned_data["end_time"].isoformat()
        self.request.session["reservation_step1_data"] = cleaned_data

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("reservation:reservation-list")


class ReservationAdminDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reservation
    template_name = "reservation/admin/reservation_delete.html"
    success_url = reverse_lazy("reservation:reservation-list")
    permission_required = "reservation.can_admin_website"


class ReservationStep1View(LoginRequiredMixin, FormView):
    template_name = "reservation/reservation1_form.html"
    form_class = ReservationStep1Form
    success_url = reverse_lazy("reservation:reservation-step2")

    def form_valid(self, form):
        # Convert date and time objects to strings before saving in the session
        cleaned_data = form.cleaned_data
        cleaned_data["date"] = cleaned_data["date"].isoformat()
        cleaned_data["start_time"] = cleaned_data["start_time"].isoformat()
        cleaned_data["end_time"] = cleaned_data["end_time"].isoformat()
        cleaned_data["user_name"] = None if self.request.user.groups.filter(name="Manager").exists() else self.request.user.full_name
        cleaned_data["user_phone"] = None if self.request.user.groups.filter(name="Manager").exists() else self.request.user.phone_number
        self.request.session["reservation_step1_data"] = cleaned_data
        return super().form_valid(form)


class ReservationStep2View(LoginRequiredMixin, FormView):
    template_name = "reservation/reservation2_form.html"
    form_class = ReservationStep2Form
    success_url = reverse_lazy("reservation:reservation-list")

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
            user_name=step1_data.get("user_name"),
            user_phone=step1_data.get("user_phone"),

        )

        # Mark the table as reserved
        table.is_reserved = True
        table.save()

        # Clear session data after successful reservation
        del self.request.session["reservation_step1_data"]

        return super().form_valid(form)