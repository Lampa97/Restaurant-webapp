from django.core.cache import cache

from config.settings import CACHE_ENABLED

from .models import Meal, MealCategory

CACHE_TIMEOUT = 60 * 15  # 15 minutes


class MealService:

    @staticmethod
    def get_all_meals_in_category(category):
        if CACHE_ENABLED:
            key = f"meals_in_category_{category}"
            meals = cache.get(key)
            if meals is not None:
                return meals
            meals = Meal.objects.filter(category=category)
            cache.set(key, meals, CACHE_TIMEOUT)
            return meals
        return Meal.objects.filter(category=category)


class MealCategoryService:

    @staticmethod
    def get_all_categories():
        if CACHE_ENABLED:
            key = "categories"
            categories = cache.get(key)
            if categories is not None:
                return categories
            categories = MealCategory.objects.all()
            cache.set(key, categories, CACHE_TIMEOUT)
            return categories
        return MealCategory.objects.all()
