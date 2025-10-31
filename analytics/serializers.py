from rest_framework import serializers
from .models import Click


class ClickSerializer(serializers.ModelSerializer):
    url_short_code = serializers.CharField(source='url.short_code', read_only=True)
    
    class Meta:
        model = Click
        fields = ['id', 'url_short_code', 'clicked_at', 'ip_address', 
                  'referer', 'country', 'city', 'device_type', 'browser', 'os']
        read_only_fields = fields


class ClickStatsSerializer(serializers.Serializer):
    total_clicks = serializers.IntegerField()
    unique_ips = serializers.IntegerField()
    device_breakdown = serializers.DictField()
    browser_breakdown = serializers.DictField()
    os_breakdown = serializers.DictField()
    daily_clicks = serializers.ListField()
