from django.contrib import admin

from .models import Table, Reservation


@admin.register(Table)
class CategoryTable(admin.ModelAdmin):
    list_display = ("number", "capacity")
    search_fields = ("number", "capacity")
    list_filter = ("capacity",)

@admin.register(Reservation)
class CategoryReservation(admin.ModelAdmin):
    list_display = ("table", "customer", "date", "start_time", "end_time", "total_persons")
    search_fields = ("table", "customer", "date", "start_time", "end_time", "total_persons")
    list_filter = ("customer", "date", "start_time", "end_time", "total_persons")
