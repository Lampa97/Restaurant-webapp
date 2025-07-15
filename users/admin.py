from django.contrib import admin

from .models import User


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "full_name", "had_booked", "is_active", "is_staff")
    search_fields = ("email", "full_name", "had_booked")
    list_filter = ("had_booked",)
