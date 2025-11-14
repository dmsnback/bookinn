from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, viewsets

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
from rooms.models import Booking, Room, RoomImage, RoomType


@extend_schema(tags=["RoomType"], summary="Управление типами номеров")
class RoomTypeViewSet(viewsets.ModelViewSet):
    """Позволяет администратору создавать, изменять и удалять типы номеров,
    например "Стандарт", "Люкс" и т.п.
    Обычные пользователи могут только просматривать список.
    """

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = (permissions.IsAdminUser,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ("name",)


@extend_schema(tags=["RoomImage"])
class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageWriteSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RoomImageReadSerializer
        return RoomImageWriteSerializer


@extend_schema(
    tags=["Room"],
    summary="Работа с номерами",
)
class RoomViewSet(viewsets.ModelViewSet):
    """Позволяет просматривать список доступных номеров,
    а администраторам — добавлять и изменять номера.
    Каждый номер связан с типом номера и может содержать фото.
    """

    serializer_class = RoomWriteSerializer
    permission_classes = (permissions.AllowAny, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("room_type", "is_available", "number_of_rooms", "capacity")
    search_fields = ("title", "description", "room_type__name")
    ordering_fields = (
        "title",
        "room_type",
        "is_available",
        "price",
        "number_of_rooms",
        "capacity",
    )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RoomReadSerializer
        return RoomWriteSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Room.objects.all()
        return Room.objects.filter(is_available=True)


@extend_schema(tags=["Booking"], summary="Работа с бронированиями")
class BookingViewSet(viewsets.ModelViewSet):
    """Пользователь может создавать, изменять и удалять свои бронирования.
    Администратор может управлять всеми бронированиями.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingWriteSerializer

    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("status", "room", "user")
    search_fields = ("status",)
    ordering_fields = ("status", "check_in", "check_out")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return BookingReadSerializer
        return BookingWriteSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
