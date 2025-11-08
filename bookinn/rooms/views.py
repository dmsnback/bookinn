from rest_framework import permissions, viewsets

from rooms.models import Booking, Room, RoomType
from rooms.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from rooms.serializers import (
    BookingSerializer,
    RoomSerializer,
    RoomTypeSerializer
)


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = (permissions.IsAdminUser,)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = (permissions.AllowAny, IsAdminOrReadOnly)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Room.objects.all()
        return Room.objects.filter(is_available=True)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
