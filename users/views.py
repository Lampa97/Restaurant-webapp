import secrets

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, View
from django.views.generic.edit import FormView

from .forms import CustomLoginForm, CustomUserCreationForm, PasswordResetConfirmForm, PasswordResetRequestForm
from .logger import users_logger
from .models import User


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    users_logger.info(f"User {user} confirmed email.")
    messages.success(request, "You successfully confirmed your email. Now you can login.")
    return redirect(reverse("users:login"))


class AdminPanelView(TemplateView):
    template_name = "users/admin_panel.html"


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

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        users_logger.info(f"User {user} registered.")
        host = self.request.get_host()
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
