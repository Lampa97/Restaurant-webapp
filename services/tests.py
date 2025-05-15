from django.test import TestCase
from django.urls import reverse
from services.models import Meal, MealCategory

class TestMealCategoryModel(TestCase):
    def setUp(self):
        self.category = MealCategory.objects.create(
            name="Appetizers",
            description="Starters to begin your meal",
        )

    def test_meal_category_creation(self):
        self.assertEqual(self.category.name, "Appetizers")
        self.assertEqual(str(self.category), "Appetizers")


class TestMealModel(TestCase):
    def setUp(self):
        self.category = MealCategory.objects.create(
            name="Main Course",
            description="Main dishes for your meal",
        )
        self.meal = Meal.objects.create(
            name="Grilled Chicken",
            description="Delicious grilled chicken",
            price=12.99,
            category=self.category,
        )

    def test_meal_creation(self):
        self.assertEqual(self.meal.name, "Grilled Chicken")
        self.assertEqual(str(self.meal), "Grilled Chicken - 12.99")

    class TestMealCategoryViews(TestCase):
        def setUp(self):
            self.category = MealCategory.objects.create(
                name="Desserts",
                description="Sweet treats to end your meal",
            )

        def test_meal_category_list_status_code(self):
            url = reverse('mealcategory-list')  # Replace with your actual URL name
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_meal_category_detail_status_code(self):
            url = reverse('mealcategory-detail', args=[self.category.id])  # Replace with your actual URL name
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    class TestMealViews(TestCase):
        def setUp(self):
            self.category = MealCategory.objects.create(
                name="Beverages",
                description="Drinks to accompany your meal",
            )
            self.meal = Meal.objects.create(
                name="Lemonade",
                description="Refreshing lemonade",
                price=3.99,
                category=self.category,
            )

        def test_meal_list_status_code(self):
            url = reverse('meal-list')  # Replace with your actual URL name
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

        def test_meal_detail_status_code(self):
            url = reverse('meal-detail', args=[self.meal.id])  # Replace with your actual URL name
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)