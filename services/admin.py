from django.contrib import admin

from .models import MealCategory, Meal


@admin.register(MealCategory)
class CategoryMealCategory(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Meal)
class CategoryMeal(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    search_fields = ("name",)
    list_filter = ("category",)