# Generated by Django 5.2 on 2025-04-29 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0005_alter_mealcategory_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mealcategory",
            name="image",
            field=models.ImageField(default="static/images/default_food.png", upload_to="menu/", verbose_name="Image"),
        ),
    ]
