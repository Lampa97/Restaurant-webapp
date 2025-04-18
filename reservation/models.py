from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Table(models.Model):
    HALL = "Hall"
    BANQUET = "Banquet"

    LOCATION_CHOICES = [(HALL, "Hall"), (BANQUET, "Banquet")]

    number = models.SmallIntegerField(unique=True, verbose_name="Table Number")
    capacity = models.SmallIntegerField(
        verbose_name="Capacity", validators=[MinValueValidator(2), MaxValueValidator(20)]
    )
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, verbose_name="Location")

    class Meta:
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} - {self.location}. Capacity: {self.capacity}"


class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations", verbose_name="Table")
    date = models.DateField(verbose_name="Reservation Date")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations", verbose_name="Customer")
    total_persons = models.PositiveIntegerField(verbose_name="Total Persons", validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ["date", "start_time"]

    def clean(self):
        # Ensure total_persons does not exceed the table's capacity
        if self.total_persons > self.table.capacity:
            raise ValidationError(f"Total persons ({self.total_persons}) cannot exceed the table's capacity ({self.table.capacity}).")

    def __str__(self):
        return f"Reservation for {self.customer} on {self.date} at {self.start_time}"