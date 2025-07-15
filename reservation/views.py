from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from .forms import ReservationStep1Form, ReservationStep2Form, TableForm
from .models import Reservation, Table

CACHE_TIMEOUT = settings.CACHE_TIMEOUT if settings.CACHE_ENABLED else 0


class TableListView(PermissionRequiredMixin, ListView):
    model = Table
    template_name = "reservation/admin/table_list.html"
    context_object_name = "tables"
    permission_required = "reservation.can_admin_website"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tables = context["tables"]
        table_reservations = {table: table.reservations.all() for table in tables}
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


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class ReservationAdminListView(PermissionRequiredMixin, ListView):
    model = Reservation
    template_name = "reservation/admin/reservation_list.html"
    context_object_name = "reservations"
    permission_required = "reservation.can_admin_website"


class ReservationAdminStep1UpdateView(PermissionRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationStep1Form
    template_name = "reservation/admin/reservation1_form_update.html"

    def get_permission_required(self):
        # Check if the user is a manager or admin
        if self.request.user.groups.filter(name="Manager").exists():
            return ["reservation.can_admin_website"]
        else:
            return []

    def form_valid(self, form):
        # Get the cleaned data
        cleaned_data = form.cleaned_data
        date = cleaned_data["date"]
        start_time = cleaned_data["start_time"]
        end_time = cleaned_data["end_time"]
        total_persons = cleaned_data.get("total_persons")
        table = self.object.table  # Get the table associated with the reservation

        # Check if total_persons exceeds the table capacity
        if total_persons > table.capacity:
            form.add_error("total_persons", f"Total persons cannot exceed the table capacity of {table.capacity}.")
            return self.form_invalid(form)

        # Check if the reservation duration exceeds 4 hours
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        duration = (end_datetime - start_datetime).total_seconds() / 3600
        if duration > 4:
            form.add_error("end_time", "Reservation duration cannot exceed 4 hours.")
            return self.form_invalid(form)

        # Check if the user already has a reservation for the selected date
        if Reservation.objects.filter(user=self.object.user, date=date).exclude(pk=self.object.pk).exists():
            form.add_error("date", "This user already has a reservation for this date.")
            return self.form_invalid(form)

        # Convert date and time objects to strings before saving in the session
        cleaned_data["date"] = date.isoformat()
        cleaned_data["start_time"] = start_time.isoformat()
        cleaned_data["end_time"] = end_time.isoformat()
        self.request.session["reservation_step1_data"] = cleaned_data

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.groups.filter(name="Manager").exists():
            return reverse_lazy("reservation:reservation-list")
        else:
            return reverse_lazy("users:user-reservations")


class ReservationAdminDeleteView(PermissionRequiredMixin, DeleteView):
    model = Reservation
    template_name = "reservation/admin/reservation_delete.html"
    success_url = reverse_lazy("reservation:reservation-list")
    permission_required = "reservation.can_admin_website"

    def delete(self, request, *args, **kwargs):
        user = self.object.user
        user_reservations = Reservation.objects.filter(user=user, is_active=True)
        if user_reservations.count() < 1:
            user.had_booked = False
            user.save()


class ReservationStep1View(LoginRequiredMixin, FormView):
    template_name = "reservation/reservation1_form.html"
    form_class = ReservationStep1Form
    success_url = reverse_lazy("reservation:reservation-step2")

    def form_valid(self, form):

        # Convert date and time objects to strings before saving in the session
        cleaned_data = form.cleaned_data
        date = cleaned_data["date"]
        start_time = cleaned_data["start_time"]
        end_time = cleaned_data["end_time"]

        # Check if the reservation duration exceeds 4 hours
        start_datetime = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)
        duration = (end_datetime - start_datetime).total_seconds() / 3600
        if duration > 4:
            form.add_error("end_time", "Reservation duration cannot exceed 4 hours.")
            return self.form_invalid(form)

        # Check if the user already has a reservation for the selected date
        if Reservation.objects.filter(user=self.request.user, date=date).exists():
            form.add_error("date", "You already have a reservation for this date.")
            return self.form_invalid(form)

        cleaned_data["date"] = cleaned_data["date"].isoformat()
        cleaned_data["start_time"] = cleaned_data["start_time"].isoformat()
        cleaned_data["end_time"] = cleaned_data["end_time"].isoformat()
        cleaned_data["user_name"] = (
            None if self.request.user.groups.filter(name="Manager").exists() else self.request.user.full_name
        )
        cleaned_data["user_phone"] = (
            None if self.request.user.groups.filter(name="Manager").exists() else self.request.user.phone_number
        )
        self.request.session["reservation_step1_data"] = cleaned_data
        return super().form_valid(form)


class ReservationStep2View(LoginRequiredMixin, FormView):
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
        if not available_tables.exists():
            messages.error(self.request, "No tables are available for the selected time and date.")
            return HttpResponseRedirect(reverse_lazy("reservation:reservation-step1"))
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

        user = self.request.user
        user.had_booked = True
        user.save()
        messages.success(
            self.request,
            f"""Reservation created successfully: Table № {table.number}, {step1_data['date']},
{step1_data['start_time']} - {step1_data['end_time']}. Total Persons: {step1_data['total_persons']}.""",
        )
        # Clear session data after successful reservation
        del self.request.session["reservation_step1_data"]

        return super().form_valid(form)
