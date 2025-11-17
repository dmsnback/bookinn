import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, serializers, viewsets

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

logger = logging.getLogger("rooms")


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

    def get_queryset(self):
        try:
            queryset = RoomType.objects.all()
            logger.info(f"Запрошены типы номеров, всего найдено: {queryset.count()}")
            return queryset
        except Exception as error:
            logger.debug(f"Ошибка при получении типов номеров: {error}", exc_info=True)
            return RoomType.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save()
            logger.info(f"Создан новый тип номера: {serializer.instance.name}")
        except Exception as error:
            logger.error(f"Ошибка при создании типа номера: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось создать тип номера"})

    def perform_update(self, serializer):
        try:
            serializer.save()
            logger.info(f"Обновлеен тип номера: {serializer.instance.name}")
        except Exception as error:
            logger.error(f"Ошибка при обновлении типа номера: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось обновить тип номера"})

    def perform_destroy(self, instance):
        try:
            room_type_name = instance.name
            instance.delete()
            logger.info(f"Удален тип номера: {room_type_name}")
        except Exception as error:
            logger.error(f"Ошибка при удалении типа номера: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось удалить тип номера"})


@extend_schema(tags=["RoomImage"])
class RoomImageViewSet(viewsets.ModelViewSet):
    queryset = RoomImage.objects.all()
    serializer_class = RoomImageWriteSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        try:
            if self.action in ["list", "retrieve"]:
                logger.debug(
                    f"Используется RoomImageReadSerializer для действия {self.action}"
                )
                return RoomImageReadSerializer
            logger.debug(
                f"Используется RoomImageWriteSerializer для действия {self.action}"
            )
            return RoomImageWriteSerializer
        except Exception as error:
            logger.error(
                f"Ошибка при выборе сериализатора для RoomImage: {error}", exc_info=True
            )
            return RoomImageWriteSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
            logger.info(
                f"Загружена новая фотография id = {serializer.instance.id} для номера {serializer.instance.room}"
            )
        except Exception as error:
            logger.error(f"Ошибка при загрузке фотогрвфии: {error}", exc_info=True)
            raise serializers.ValidationError(
                {"error": "Не удалось загрузить фотографию"}
            )

    def perform_update(self, serializer):
        try:
            serializer.save()
            logger.info(f"Фотография обновлена id = {serializer.instance.id}")
        except Exception as error:
            logger.error(f"Ошибка при обновлении фотографии: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось обновить фотографию"})

    def perform_destroy(self, instance):
        try:
            image_name = instance.image
            instance.delete()
            logger.info(f"Фотография удалена: {image_name}")
        except Exception as error:
            logger.error(f"Ошибка при удалении фотографии: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось удалить фотографию"})


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
        try:
            if self.action in ["list", "retrieve"]:
                logger.debug(
                    f"Используется RoomReadSerializer для действия {self.action}"
                )
                return RoomReadSerializer
            logger.debug(f"Используется RoomWriteSerializer для действия {self.action}")
            return RoomWriteSerializer
        except Exception as error:
            logger.error(
                f"Ошибка при выборе сериализатора для Room: {error}", exc_info=True
            )
            return RoomWriteSerializer

    def get_queryset(self):
        try:
            if self.request.user.is_staff or self.request.user.is_superuser:
                queryset = Room.objects.all()
            else:
                queryset = Room.objects.filter(is_available=True)
            logger.debug(f"Запрошены номера, всего найдено: {queryset.count()}")
            return queryset
        except Exception as error:
            logger.error(f"Ошибка при получении списка номеров: {error}", exc_info=True)
            return Room.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save()
            logger.info(f"Добавлен новый номер: {serializer.instance.title}")
        except Exception as error:
            logger.error(f"Ошибка при добавлении номера: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось добавить номер"})

    def perform_update(self, serializer):
        try:
            serializer.save()
            logger.info(f"Номер обновлен {serializer.instance.title}")
        except Exception as error:
            logger.error(f"Ошибка при обновлении номера: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось обновить номер"})

    def perform_destroy(self, instance):
        try:
            room_name = instance.title
            instance.delete()
            logger.info(f"Номер {room_name} удален")
        except Exception as error:
            logger.error(f"Ошибка при удалении номера: {error}", exc_info=True)
            raise serializers.ValidationError({"error": "Не удалось удалить номер"})


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
        try:
            if self.action in ["list", "retrieve"]:
                logger.debug(
                    f"Используется BookingReadSerializer для действия {self.action}"
                )
                return BookingReadSerializer
            logger.debug(
                f"Используется BookingWriteSerializer для действия {self.action}"
            )
            return BookingWriteSerializer
        except Exception as error:
            logger.error(
                f"Ошибка при выборе сериализатора для Booking: {error}", exc_info=True
            )
            return BookingWriteSerializer

    def get_queryset(self):
        try:
            if self.request.user.is_staff or self.request.user.is_superuser:
                queryset = Booking.objects.all()
            else:
                queryset = Booking.objects.filter(user=self.request.user)
                logger.debug(
                    f"Запрошены бронирования пользователем: {self.request.user}, найдеено бронирований: {queryset.count()}"
                )
            return queryset
        except Exception as error:
            logger.error(
                f"Ошибка при получении списка бронирований: {error}", exc_info=True
            )
            return Booking.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
            logger.info(
                f"Пользователь {self.request.user} создал бронирование для номера: {serializer.instance.room}"
            )
        except Exception as error:
            logger.error(f"Не удалось создать бронирование: {error}", exc_info=True)
            raise serializers.ValidationError(
                {"error": "Не Удалось создать бронирование"}
            )

    def perform_update(self, serializer):
        try:
            serializer.save(user=self.request.user)
            logger.info(
                f"Пользователь {self.request.user} обновил бронирование для номера: {serializer.instance.room}"
            )
        except Exception as error:
            logger.error(f"Ошибка при обновлении бронирования: {error}", exc_info=True)
            raise serializers.ValidationError(
                {"error": "Не удалось обновить бронирование"}
            )

    def perform_destroy(self, instance):
        try:
            booking_for_room = instance.room
            instance.delete()
            logger.info(f"Бронирование для номера {booking_for_room} удалено")
        except Exception as error:
            logger.error(f"Ошибка при удалении бронирования: {error}", exc_info=True)
            raise serializers.ValidationError(
                {"error": "Не удалось удалить бронирование"}
            )
