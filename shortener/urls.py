from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import URLViewSet, redirect_url

router = DefaultRouter()
router.register(r'urls', URLViewSet, basename='url')

urlpatterns = [
    path('api/', include(router.urls)),
    path('<str:short_code>/', redirect_url, name='redirect'),
]
