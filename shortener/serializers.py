from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    clicks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_code', 'short_url', 'created_at', 
                  'expires_at', 'is_active', 'custom_alias', 'clicks_count']
        read_only_fields = ['short_code', 'created_at', 'clicks_count']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/{obj.short_code}')
        return f'/{obj.short_code}'
    
    def get_clicks_count(self, obj):
        return obj.clicks.count()


class URLCreateSerializer(serializers.ModelSerializer):
    custom_code = serializers.CharField(max_length=10, required=False, allow_blank=True)
    
    class Meta:
        model = URL
        fields = ['original_url', 'custom_code', 'expires_at']
    
    def validate_custom_code(self, value):
        if value and URL.objects.filter(short_code=value).exists():
            raise serializers.ValidationError("This custom code is already taken.")
        return value
    
    def create(self, validated_data):
        custom_code = validated_data.pop('custom_code', None)
        user = self.context['request'].user if self.context['request'].user.is_authenticated else None
        
        url = URL(
            original_url=validated_data['original_url'],
            expires_at=validated_data.get('expires_at'),
            user=user
        )
        
        if custom_code:
            url.short_code = custom_code
            url.custom_alias = True
        
        url.save()
        return url
