from django.contrib import admin


from .models import *


@admin.register(Films)
class FilmsAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'time_release',
                    'description',
                    'category',)
    list_filter = ('time_release', 'category', )
    list_display_links = ('name',)
    search_fields = ('name', 'time_release', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Directors)
class DirectorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_display_links = ('name',)


