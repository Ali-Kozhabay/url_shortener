from django.contrib import admin
from .models import Click


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ['url', 'clicked_at', 'ip_address', 'device_type', 'browser', 'os']
    list_filter = ['device_type', 'browser', 'os', 'clicked_at']
    search_fields = ['url__short_code', 'ip_address']
    readonly_fields = ['clicked_at']
    date_hierarchy = 'clicked_at'
