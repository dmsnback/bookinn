from rest_framework import viewsets

from rooms.models import Booking, Room, RoomType
from rooms.serializers import (
    BookingSerializer,
    RoomSerializer,
    RoomTypeSerializer
)


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
