import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from django.views.generic.edit import FormView

from reservation.models import Reservation

from .forms import (
    CustomLoginForm,
    CustomUserCreationForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    UserUpdateForm,
)
from .logger import users_logger
from .models import User
from .services import get_closest_booking_date

CACHE_TIMEOUT = settings.CACHE_TIMEOUT if settings.CACHE_ENABLED else 0


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    users_logger.info(f"User {user} confirmed email.")
    messages.success(request, "You successfully confirmed your email. Now you can login.")
    return redirect(reverse("users:login"))


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class PersonalCabinetView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/personal_cabinet/personal_cabinet.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["closest_booking_date"] = get_closest_booking_date(self.request.user)
        return context


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/personal_cabinet/edit_profile.html"

    def get_success_url(self):
        return reverse_lazy("users:personal-cabinet", kwargs={"pk": self.object.pk})


class UserReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "users/personal_cabinet/user_reservation_list.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, is_active=True).order_by("-date", "-start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class CancelReservationView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = "users/personal_cabinet/cancel_reservation.html"

    def get_success_url(self):
        messages.success(self.request, "Reservation successfully canceled.")
        return reverse_lazy("users:personal-cabinet", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        """Changing the status of user(had_booked) to False if he has no active reservations"""
        user = self.request.user
        user_reservations = Reservation.objects.filter(user=user, is_active=True)
        if user_reservations.count() < 1:
            user.had_booked = False
            user.save()
        return super().delete(request, *args, **kwargs)


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "users/personal_cabinet/booking_history.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("-date", "-start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class AdminPanelView(PermissionRequiredMixin, TemplateView):
    template_name = "users/admin/admin_panel.html"
    permission_required = "users.can_admin_website"


class ChangeUserStatusView(PermissionRequiredMixin, View):
    permission_required = "users.can_block_user"

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user == request.user:
            messages.warning(request, "You cannot block yourself.")
            return redirect("users:all-users")
        user.is_active = not user.is_active
        user.save()
        users_logger.info(f"User {user} status changed.")
        return redirect("users:all-users")


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class BookingHistoryAdminView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "users/admin/booking_history.html"
    context_object_name = "reservations"

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return Reservation.objects.filter(user=user).order_by("-date", "-start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, id=self.kwargs["user_id"])
        return context


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class UsersListView(PermissionRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    permission_required = "users.can_admin_website"

    def get(self, request):
        all_users = User.objects.filter(is_staff=False, is_superuser=False)
        paginator = Paginator(all_users, 10)  # Show 10 users per page

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        for user in page_obj:
            reservation = Reservation.objects.filter(user=user, is_active=True).first()
            user.table = reservation.table if reservation else None
            user.reservation_date = reservation.date if reservation else None

        context = {"users": page_obj}
        return render(request, "users/admin/users_list.html", context)


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("restaurant:home")
    authentication_form = CustomLoginForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("restaurant:home")


class RegisterView(FormView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("restaurant:home")

    def get_success_url(self):
        messages.success(
            self.request,
            """Registration successful. Please check your email to confirm your account.
            If you don't see the email, please check your spam folder.""",
        )

        return reverse_lazy("restaurant:home")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        users_logger.info(f"User {user} registered.")
        host = self.request.get_host()
        if host.startswith("django"):
            host = settings.SERVER_IP
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Email confirmation",
            message=f"Hi! Please follow the link to confirm your email {url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        users_logger.info(f"Email confirmation sent to {user}.")
        return super().form_valid(form)


class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetRequestForm()
        return render(request, "users/password_reset_request.html", {"form": form})

    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data["email"])
            host = self.request.get_host()
            token = secrets.token_hex(16)
            user.password_reset_token = token
            user.save()
            users_logger.info(f"User {user} requested password reset.")
            reset_url = f"{host}/users/reset-password-confirm/{token}/"
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            users_logger.info(f"Password reset request sent to {user}.")
            messages.success(request, "Password reset request sent to your email account.")
            return redirect("users:login")
        return render(request, "users/password_reset_request.html", {"form": form})


class PasswordResetConfirmView(View):
    """
    Handles password reset confirmation for users.

    Methods:
        get(request, token): Renders the password reset confirmation form.
        post(request, token): Processes the password reset form and updates the user's password.
    """

    def get(self, request, token):
        user = get_object_or_404(User, password_reset_token=token)
        form = PasswordResetConfirmForm()
        return render(
            request, "users/password_reset_confirm.html", {"form": form, "token": token, "email": user.email}
        )

    def post(self, request, token):
        user = get_object_or_404(User, password_reset_token=token)
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.password_reset_token = None
            user.save()
            users_logger.info(f"User {user} password reset.")
            messages.success(request, "Your new password is successfully set.")
            return redirect("users:login")
        return render(request, "users/password_reset_confirm.html", {"form": form, "token": token})
