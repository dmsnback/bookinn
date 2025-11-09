from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

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
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = (permissions.AllowAny, IsAdminOrReadOnly)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = (
        'room_type',
        'is_available',
        'number_of_rooms',
        'capacity'
    )
    search_fields = ('title', 'description', 'room_type__name')
    ordering_fields = (
        'title',
        'room_type',
        'is_available',
        'price',
        'number_of_rooms',
        'capacity'
    )

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Room.objects.all()
        return Room.objects.filter(is_available=True)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('status', 'room', 'user')
    search_fields = ('status',)
    ordering_fields = ('status', 'check_in', 'check_out')

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
