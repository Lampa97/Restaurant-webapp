from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates Manager group and assigns 'can_admin_website' permission to all models"

    def handle(self, *args, **options):
        # Create the Manager group
        managers_group, created = Group.objects.get_or_create(name="Manager")

        # Iterate through all models
        for model in apps.get_models():
            content_type = ContentType.objects.get_for_model(model)
            permission, _ = Permission.objects.get_or_create(
                codename="can_admin_website",
                name="Can administer the website",
                content_type=content_type,
            )
            managers_group.permissions.add(permission)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created Group {managers_group.name} and assigned permissions")
        )
