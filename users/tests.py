from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse

from reservation.models import Reservation, Table

User = get_user_model()


class TestUsersViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com",
            password="password123",
            is_active=True,
        )
        self.admin_user = User.objects.create(
            email="adminuser@example.com",
            password="adminpassword",
        )
        self.table = Table.objects.create(
            number=1,
            capacity=4,
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=date.today() + timedelta(days=1),
            start_time="18:00:00",
            end_time="20:00:00",
            is_active=True,
            total_persons=4,
            table_id=self.table.pk,
        )

        # Add admin_user to a group with required permissions
        managers_group, created = Group.objects.get_or_create(name="Manager")
        permissions = Permission.objects.filter(
            codename__in=[
                "can_admin_website",
            ]
        )
        managers_group.permissions.add(*permissions)
        managers_group.user_set.add(self.admin_user)

    def test_personal_cabinet_view_status_code(self):
        self.client.force_login(self.user)
        url = reverse("users:personal-cabinet", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_view_status_code(self):
        self.client.force_login(self.user)
        url = reverse("users:user-profile-update", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_reservation_list_view_status_code(self):
        self.client.force_login(self.user)
        url = reverse("users:user-reservations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cancel_reservation_view_status_code(self):
        self.client.force_login(self.user)
        url = reverse("users:cancel-reservation", kwargs={"pk": self.reservation.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_booking_history_view_status_code(self):
        self.client.force_login(self.user)
        url = reverse("users:booking-history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_panel_view_status_code(self):
        self.client.force_login(self.admin_user)
        url = reverse("users:admin")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_users_list_view_status_code(self):
        self.client.force_login(self.admin_user)
        url = reverse("users:all-users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
