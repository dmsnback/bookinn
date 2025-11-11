from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    BookingViewSet,
    RoomViewSet,
    RoomImageViewSet,
    RoomTypeViewSet
)


v1_router = DefaultRouter()
v1_router.register(r'rooms', RoomViewSet, basename='rooms')
v1_router.register(r'room_type', RoomTypeViewSet)
v1_router.register(r'bookings', BookingViewSet, basename='bookings')
v1_router.register(r'room_images', RoomImageViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
