from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", views.email_verification, name="email-confirm"),
    path("reset-password/", views.PasswordResetRequestView.as_view(), name="reset-password"),
    path(
        "reset-password-confirm/<str:token>/", views.PasswordResetConfirmView.as_view(), name="reset-password-confirm"
    ),
    path("admin/", views.AdminPanelView.as_view(), name="admin"),
    path("admin/all-users/", views.UsersListView.as_view(), name="all-users"),
    path(
        "admin/user/<int:user_id>/booking-history/",
        views.BookingHistoryAdminView.as_view(),
        name="user-booking-history",
    ),
    path("admin/user/<int:pk>/change-status/", views.ChangeUserStatusView.as_view(), name="change-status"),
    path("personal-cabinet/<int:pk>/", views.PersonalCabinetView.as_view(), name="personal-cabinet"),
    path("user/<int:pk>/update/", views.EditProfileUpdateView.as_view(), name="user-profile-update"),
    path("user/reservations/", views.UserReservationListView.as_view(), name="user-reservations"),
    path("user/reservations/<int:pk>/cancel/", views.CancelReservationView.as_view(), name="cancel-reservation"),
    path("user/reservations/history/", views.BookingHistoryView.as_view(), name="booking-history"),
]
