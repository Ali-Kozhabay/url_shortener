from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Click
from .serializers import ClickSerializer, ClickStatsSerializer
from shortener.models import URL


class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ClickSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Click.objects.filter(url__user=user).select_related('url')
    
    @action(detail=False, methods=['get'], url_path='url/(?P<short_code>[^/.]+)')
    def url_stats(self, request, short_code=None):
        """Get analytics for a specific URL"""
        url = get_object_or_404(URL, short_code=short_code, user=request.user)
        
        # Get date range (default: last 30 days)
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        clicks = Click.objects.filter(url=url, clicked_at__gte=start_date)
        
        # Calculate stats
        total_clicks = clicks.count()
        unique_ips = clicks.values('ip_address').distinct().count()
        
        # Device breakdown
        device_breakdown = dict(
            clicks.values('device_type')
            .annotate(count=Count('id'))
            .values_list('device_type', 'count')
        )
        
        # Browser breakdown
        browser_breakdown = dict(
            clicks.values('browser')
            .annotate(count=Count('id'))
            .values_list('browser', 'count')
        )
        
        # OS breakdown
        os_breakdown = dict(
            clicks.values('os')
            .annotate(count=Count('id'))
            .values_list('os', 'count')
        )
        
        # Daily clicks
        daily_clicks = []
        for i in range(days):
            date = (timezone.now() - timedelta(days=i)).date()
            count = clicks.filter(clicked_at__date=date).count()
            daily_clicks.append({
                'date': date.isoformat(),
                'clicks': count
            })
        
        stats = {
            'total_clicks': total_clicks,
            'unique_ips': unique_ips,
            'device_breakdown': device_breakdown,
            'browser_breakdown': browser_breakdown,
            'os_breakdown': os_breakdown,
            'daily_clicks': daily_clicks[::-1]  # Reverse to show oldest first
        }
        
        serializer = ClickStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Get overall dashboard stats for user"""
        user = request.user
        
        total_urls = URL.objects.filter(user=user).count()
        total_clicks = Click.objects.filter(url__user=user).count()
        
        # Recent clicks
        recent_clicks = Click.objects.filter(url__user=user).order_by('-clicked_at')[:10]
        
        # Top URLs
        top_urls = (
            URL.objects.filter(user=user)
            .annotate(click_count=Count('clicks'))
            .order_by('-click_count')[:5]
        )
        
        return Response({
            'total_urls': total_urls,
            'total_clicks': total_clicks,
            'recent_clicks': ClickSerializer(recent_clicks, many=True).data,
            'top_urls': [
                {
                    'short_code': url.short_code,
                    'original_url': url.original_url,
                    'clicks': url.click_count
                }
                for url in top_urls
            ]
        })
