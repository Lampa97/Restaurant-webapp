from django.contrib import admin

from .models import Reservation, Table


@admin.register(Table)
class CategoryTable(admin.ModelAdmin):
    list_display = ("number", "capacity")
    search_fields = ("number", "capacity")
    list_filter = ("capacity",)


@admin.register(Reservation)
class CategoryReservation(admin.ModelAdmin):
    list_display = ("table", "user", "date", "start_time", "end_time", "total_persons", "is_active")
    search_fields = ("table", "user", "date", "start_time", "end_time", "total_persons")
    list_filter = ("user", "date", "start_time", "end_time", "total_persons", "is_active")
