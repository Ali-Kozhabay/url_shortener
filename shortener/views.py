from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .models import URL
from .serializers import URLSerializer, URLCreateSerializer
from analytics.tasks import track_click


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return URLCreateSerializer
        return URLSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return URL.objects.filter(user=self.request.user, is_active=True)
        return URL.objects.filter(is_active=True, user=None)
    
    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST'))
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Cache the URL
        url_obj = serializer.instance
        cache.set(f'url:{url_obj.short_code}', url_obj.original_url, timeout=60*60*24)
        
        response_serializer = URLSerializer(url_obj, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        url = self.get_object()
        url.is_active = False
        url.save()
        
        # Remove from cache
        cache.delete(f'url:{url.short_code}')
        
        return Response({'status': 'URL deactivated'})


@api_view(['GET'])
def redirect_url(request, short_code):
    """Redirect to original URL and track analytics"""
    
    # Try to get from cache first
    original_url = cache.get(f'url:{short_code}')
    
    if not original_url:
        # Get from database
        url_obj = get_object_or_404(URL, short_code=short_code, is_active=True)
        
        # Check if expired
        if url_obj.expires_at and url_obj.expires_at < timezone.now():
            return Response({'error': 'URL has expired'}, status=status.HTTP_410_GONE)
        
        original_url = url_obj.original_url
        
        # Cache it
        cache.set(f'url:{short_code}', original_url, timeout=60*60*24)
    else:
        # Still need URL object for tracking
        url_obj = get_object_or_404(URL, short_code=short_code)
    
    # Track click asynchronously
    track_click.delay(
        url_id=url_obj.id,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referer=request.META.get('HTTP_REFERER', '')
    )
    
    return redirect(original_url)


def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
