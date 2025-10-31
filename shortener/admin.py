from django.contrib import admin
from .models import URL


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ['short_code', 'original_url', 'user', 'created_at', 'is_active', 'custom_alias']
    list_filter = ['is_active', 'custom_alias', 'created_at']
    search_fields = ['short_code', 'original_url', 'user__username']
    readonly_fields = ['created_at', 'short_code']
    date_hierarchy = 'created_at'
