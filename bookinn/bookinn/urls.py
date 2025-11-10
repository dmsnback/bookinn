from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rooms.views import (
    BookingViewSet,
    RoomViewSet,
    RoomImageViewSet,
    RoomTypeViewSet
)


router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'room_type', RoomTypeViewSet)
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'room_images', RoomImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
