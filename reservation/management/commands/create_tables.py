from django.core.management.base import BaseCommand
from restaurant.models import Table

class Command(BaseCommand):
    help = "Create tables with predefined configurations"

    def handle(self, *args, **kwargs):
        table_configurations = [
            (1, 6, 2),  # Numbers 1-6, 2-person tables
            (7, 12, 4),  # Numbers 7-12, 4-person tables
            (13, 16, 6),  # Numbers 13-16, 6-person tables
            (17, 18, 8),  # Numbers 17-18, 8-person tables
            (19, 20, 10),  # Numbers 19-20, 10-person tables
        ]

        for start, end, capacity in table_configurations:
            for number in range(start, end + 1):
                Table.objects.create(number=number, capacity=capacity)
                self.stdout.write(self.style.SUCCESS(f"Table {number} with capacity {capacity} created."))