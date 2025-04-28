from django.db import models


class MealCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to="menu/", verbose_name="Image")

    class Meta:
        verbose_name = "Meal Category"
        verbose_name_plural = "Meal Categories"
        ordering = ["pk"]

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to="meals/", verbose_name="Image", default="static/default_food.png")
    category = models.ForeignKey(
        MealCategory, on_delete=models.CASCADE, related_name="meals", verbose_name="Menu Category"
    )

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meals"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.price}"
