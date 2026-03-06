from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



router = DefaultRouter()

# Registering History ViewSets
router.register(r'alert-history', AlertsHistoryViewSet, basename='alert-history')
router.register(r'announcement-history', AnnouncementHistoryViewSet, basename='announcement-history')
router.register(r'greeting-banner-history', GreetingBannerHistoryViewSet, basename='greeting-banner-history')
router.register(r'news-history', NewsHistoryViewSet, basename='news-history')

# Registering Overview ViewSets
router.register(r'alert-overview', AlertsOverviewViewSet, basename='alert-overview')
router.register(r'announcement-overview', AnnouncementOverviewViewSet, basename='announcement-overview')
router.register(r'greeting-banner-overview', GreetingBannerOverviewViewSet, basename='greeting-banner-overview')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairViewSet.as_view(), name='token_obtain_pair'),  # Use custom login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Corrected
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('teamlogout/', LogoutAPIView.as_view(), name='teamlogout'),
    path('sendnotification_cron/', SendNotificationCron.as_view(), name='sendnotification_cron'),
    path('download/announcement-image/<int:pk>/', download_announcement_file.as_view(), name='download_announcement_file'),
]
