from django.contrib import admin

from .models import Personnel, Review, Service


@admin.register(Personnel)
class CategoryPersonnel(admin.ModelAdmin):
    list_display = (
        "name",
        "position",
    )
    search_fields = (
        "name",
        "position",
    )


@admin.register(Service)
class CategoryService(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Review)
class CategoryReview(admin.ModelAdmin):
    list_display = ("name", "rating", "date")
    search_fields = ("name", "rating", "date")
    list_filter = ("rating",)
    ordering = ("date",)
