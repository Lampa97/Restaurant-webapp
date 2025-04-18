from django.contrib import admin

from .models import User


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "full_name", "is_active", "is_staff")
    search_fields = ("email", "full_name",)
