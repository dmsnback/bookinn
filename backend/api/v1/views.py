from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from rooms.models import Booking, Room, RoomImage, RoomType
from api.v1.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from api.v1.serializers import (
    BookingReadSerializer,
    BookingWriteSerializer,
    RoomImageReadSerializer,
    RoomImageWriteSerializer,
    RoomReadSerializer,
    RoomTypeSerializer,
    RoomWriteSerializer,
)


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('name',)


class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageWriteSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RoomImageReadSerializer
        return RoomImageWriteSerializer


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomWriteSerializer
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

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RoomReadSerializer
        return RoomWriteSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Room.objects.all()
        return Room.objects.filter(is_available=True)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingWriteSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    )
    filterset_fields = ('status', 'room', 'user')
    search_fields = ('status',)
    ordering_fields = ('status', 'check_in', 'check_out')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookingReadSerializer
        return BookingWriteSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
