# Generated by Django 5.2 on 2025-05-01 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0005_alter_personnel_photo"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="personnel",
            options={
                "ordering": ["name"],
                "permissions": [("can_admin_website", "Can administer the website")],
                "verbose_name": "Personnel",
                "verbose_name_plural": "Personnel",
            },
        ),
        migrations.AlterModelOptions(
            name="review",
            options={
                "ordering": ["-date"],
                "permissions": [("can_admin_website", "Can administer the website")],
                "verbose_name": "Review",
                "verbose_name_plural": "Reviews",
            },
        ),
        migrations.AlterModelOptions(
            name="service",
            options={
                "ordering": ["name"],
                "permissions": [("can_admin_website", "Can administer the website")],
                "verbose_name": "Service",
                "verbose_name_plural": "Services",
            },
        ),
    ]
