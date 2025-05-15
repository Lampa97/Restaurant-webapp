from datetime import date, datetime, time, timedelta
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from dotenv import load_dotenv

from reservation import views
from reservation.forms import ReservationStep1Form, ReservationStep2Form, TableForm
from reservation.models import Reservation, Table
from reservation.tasks import check_booking_status

load_dotenv()


class TestReservationTasks(TestCase):

    @patch("reservation.tasks.Reservation.objects.filter")
    def test_check_booking_status(self, mock_filter):
        # Mock reservations
        mock_reservation = MagicMock()
        mock_reservation.end_time = (datetime.now() - timedelta(hours=1)).time()
        mock_reservation.date = datetime.now().date()
        mock_reservation.is_active = True
        mock_filter.return_value = [mock_reservation]

        # Call the task
        check_booking_status()

        # Assertions
        mock_reservation.save.assert_called_once()
        self.assertFalse(mock_reservation.is_active)


class TestReservationModel(TestCase):

    @patch("reservation.models.Reservation.save")
    def test_reservation_model(self, mock_save):
        # Create a mock reservation
        reservation = Reservation(
            date=datetime.now().date(),
            start_time=datetime.now().time(),
            end_time=(datetime.now() + timedelta(hours=1)).time(),
            is_active=True,
        )
        reservation.save()

        # Assertions
        mock_save.assert_called_once()


class TestReservationURLs(SimpleTestCase):
    def test_reservation_list_url(self):
        url = reverse("reservation:reservation-list")
        self.assertEqual(resolve(url).func.view_class, views.ReservationAdminListView)


class TestTableForm(TestCase):
    def setUp(self):
        # Create some tables in the database
        Table.objects.create(number=1, capacity=4)
        Table.objects.create(number=2, capacity=6)

    def test_table_form_available_numbers(self):
        form = TableForm()
        available_numbers = [choice[0] for choice in form.fields["number"].choices]
        self.assertNotIn(1, available_numbers)  # Table 1 is already in the database
        self.assertNotIn(2, available_numbers)  # Table 2 is already in the database
        self.assertIn(3, available_numbers)  # Table 3 should be available


class TestReservationStep1Form(TestCase):
    def test_valid_reservation_step1_form(self):
        form_data = {
            "date": date.today(),
            "start_time": time(10, 0),
            "end_time": time(12, 0),
            "total_persons": 4,
            "user_name": "John Doe",
            "user_phone": "1234567890",
        }
        form = ReservationStep1Form(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_start_time(self):
        form_data = {
            "date": date.today(),
            "start_time": time(8, 0),  # Before allowed time
            "end_time": time(12, 0),
            "total_persons": 4,
            "user_name": "John Doe",
            "user_phone": "1234567890",
        }
        form = ReservationStep1Form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("Start time must be between", form.errors["__all__"][0])

    def test_invalid_end_time(self):
        form_data = {
            "date": date.today(),
            "start_time": time(10, 0),
            "end_time": time(9, 0),  # End time before start time
            "total_persons": 4,
            "user_name": "John Doe",
            "user_phone": "1234567890",
        }
        form = ReservationStep1Form(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("End time must be between", form.errors["__all__"][0])


class TestReservationStep2Form(TestCase):
    def setUp(self):
        # Create a table and a reservation
        self.table = Table.objects.create(number=1, capacity=4)
        self.reservation = Reservation.objects.create(
            table=self.table,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
            total_persons=4,
            user_name="John Doe",
            user_phone="1234567890",
        )

    def test_valid_reservation_step2_form(self):
        form = ReservationStep2Form(
            data={"table": self.table.id},
            available_tables=Table.objects.all(),
            initial={
                "date": date.today(),
                "start_time": time(12, 30),
                "end_time": time(14, 0),
            },
        )
        self.assertTrue(form.is_valid())

    def test_overlapping_reservation(self):
        form = ReservationStep2Form(
            data={"table": self.table.id},
            available_tables=Table.objects.all(),
            initial={
                "date": date.today(),
                "start_time": time(11, 0),  # Overlaps with existing reservation
                "end_time": time(13, 0),
            },
        )
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("The selected table is already booked from", form.errors["__all__"][0])
