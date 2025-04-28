from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm"),
    path("reset-password/", views.PasswordResetRequestView.as_view(), name="reset-password"),
    path("reset-password-confirm/<str:token>/", views.PasswordResetConfirmView.as_view(), name="reset-password-confirm"),
]
