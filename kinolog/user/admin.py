from django.contrib import admin
from .models import UserCustom


@admin.register(UserCustom)
class AdminUserCustom(admin.ModelAdmin):
    list_display = ('first_name',
                    'last_name',
                    'phone',
                    'email',)
    list_display_links = ('first_name', 'last_name',)
    list_filter = ('first_name', 'phone',)
    search_fields = ('first_name', 'phone',)
