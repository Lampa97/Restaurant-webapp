# Generated by Django 5.2 on 2025-05-01 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reservation", "0008_alter_reservation_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="reservation",
            options={
                "ordering": ["date", "start_time"],
                "permissions": [("can_admin_website", "Can administer the website")],
                "verbose_name": "Reservation",
                "verbose_name_plural": "Reservations",
            },
        ),
        migrations.AlterModelOptions(
            name="table",
            options={
                "ordering": ["number"],
                "permissions": [("can_admin_website", "Can administer the website")],
                "verbose_name": "Table",
                "verbose_name_plural": "Tables",
            },
        ),
    ]
