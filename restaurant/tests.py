from django.test import TestCase

from restaurant.forms import PersonnelForm, ReviewForm, ServiceForm
from restaurant.models import Personnel, Review, Service


# Model Tests
class TestReviewModel(TestCase):
    def setUp(self):
        self.review = Review.objects.create(name="John Doe", review_text="Great service!", rating=5)

    def test_review_creation(self):
        self.assertEqual(self.review.name, "John Doe")
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(str(self.review), "John Doe - 5")


class TestPersonnelModel(TestCase):
    def setUp(self):
        self.personnel = Personnel.objects.create(
            name="Jane Smith",
            position="Chef",
            description="Expert in Italian cuisine",
            quote="Cooking is an art.",
        )

    def test_personnel_creation(self):
        self.assertEqual(self.personnel.name, "Jane Smith")
        self.assertEqual(self.personnel.position, "Chef")
        self.assertEqual(str(self.personnel), "Jane Smith - Chef")


class TestServiceModel(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Catering",
            description="High-quality catering services",
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Catering")
        self.assertEqual(str(self.service), "Catering")


# Form Tests
class TestReviewForm(TestCase):
    def test_valid_review_form(self):
        form_data = {
            "name": "John Doe",
            "review_text": "Amazing experience!",
            "rating": 5,
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_review_form(self):
        form_data = {
            "name": "",
            "review_text": "Amazing experience!",
            "rating": 5,
        }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class TestPersonnelForm(TestCase):
    def test_valid_personnel_form(self):
        form_data = {
            "name": "Jane Smith",
            "position": "Manager",
            "description": "Oversees daily operations",
            "quote": "Leadership is key.",
        }
        form = PersonnelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_personnel_form(self):
        form_data = {
            "name": "Jane Smith",
            "position": "",
            "description": "Oversees daily operations",
            "quote": "Leadership is key.",
        }
        form = PersonnelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("position", form.errors)


class TestServiceForm(TestCase):

    def test_invalid_service_form(self):
        form_data = {
            "name": "Delivery",
            "description": "Fast and reliable delivery service",
            "image": "test_image.jpg",
            # Add any other required fields here
        }
        form = ServiceForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)
