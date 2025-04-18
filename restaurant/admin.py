from django.contrib import admin

from .models import Personnel, Service


@admin.register(Personnel)
class CategoryPersonnel(admin.ModelAdmin):
    list_display = ("name", "position",)
    search_fields = ("name", "position",)

@admin.register(Service)
class CategoryService(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
