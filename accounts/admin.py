from django.contrib import admin
from .models import Plan, UserProfile


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_urls', 'max_clicks_per_month', 'price', 'custom_alias', 'api_access']
    list_filter = ['custom_alias', 'api_access']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'created_at', 'updated_at']
    list_filter = ['plan', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
