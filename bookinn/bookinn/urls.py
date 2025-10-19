from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import include, path

from rooms.views import BookingViewSet, RoomViewSet, RoomTypeViewSet


router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'room_type', RoomTypeViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
