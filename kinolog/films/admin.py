from django.contrib import admin

from .models import Category, Directors, Films


@admin.register(Films)
class FilmsAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "time_release",
        "description",
        "category",
    )
    list_filter = (
        "time_release",
        "category",
    )
    list_display_links = ("name",)
    search_fields = (
        "name",
        "time_release",
        "category",
    )
    raw_id_fields = ("category",)
    filter_horizontal = ("directors",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(Directors)
class DirectorsAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_display_links = ("name",)
    search_fields = (
        "name",
        "description",
    )
