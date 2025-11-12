from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from rooms.utils import room_image_upload_path


User = get_user_model()


# ROOM_TYPE_CHOICES = (
#     ('Standart', 'Стандарт'),
#     ('Luxury', 'Люкс'),
#     ('President', 'Президент'),
# )


STATUS_ROOM_CHOICES = (
    ('checked_out', 'Выселен'),
    ('checked_in', 'Заселен'),
    ('booked', 'Забронировано'),
    ('cancelled', 'Отменено'),
)


class RoomType(models.Model):
    """Модель типа номера"""
    name = models.CharField(
        'Название типа номера',
        max_length=64,
        unique=True
    )
    description = models.TextField('Описание типа номера', blank=True)

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_name',
            )
        ]

    def __str__(self):
        return self.name


class Room(models.Model):
    """Информация о номере"""
    title = models.CharField('Название номера', max_length=128)
    description = models.TextField('Описание номера', blank=True)
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тип номера',
        related_name='rooms'
    )
    is_available = models.BooleanField('Статус номера', default=True)
    price = models.DecimalField(
        'Цена за сутки',
        max_digits=8,
        decimal_places=2
    )
    capacity = models.PositiveSmallIntegerField('Вместимость', default=1)
    number_of_rooms = models.PositiveSmallIntegerField(
        'Количество комнат',
        default=1
    )
    created_at = models.DateTimeField(
        'Дата создания номера',
        auto_now_add=True
    )

    class Meta:
        ordering = ['title',]
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'room_type'],
                name='unique_title',
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.room_type}'

    def is_available_for_period(
            self,
            check_in,
            check_out,
            exclude_booking=None
    ):
        '''Вернет True, если номер свободен на указанный период'''
        bookings = self.bookings.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exclude(status='cancelled')
        if exclude_booking:
            bookings = bookings.exclude(pk=exclude_booking.pk)
        return not bookings.exists()


class RoomImage(models.Model):
    """Фотографии номеров"""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Номер',
        help_text='Номер к которому привязано фото'
    )
    image = models.ImageField(
        'Фотография',
        upload_to=room_image_upload_path,
        help_text='Загрузите фотографию'
    )
    uploaded_at = models.DateTimeField(
        'Дата загрузки фото',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Фотография номера'
        verbose_name_plural = 'Фотографии номеров'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'Фотография для: {self.room.title}'

    def image_tag(self):
        """Миниатюра фотографии в админке"""
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" '
                f'width="100" style="border-radius: 8px;"/>'
            )
        return 'Нет фотографий номера'
    image_tag.allow_tags = True
    image_tag.short_description = 'Превью'


class Booking(models.Model):
    """Модель бронирования номера"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Гость'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='Номер'
    )
    check_in = models.DateField('Дата заезда')
    check_out = models.DateField('Дата выселения')
    status = models.CharField(
        'Статус брони',
        max_length=64,
        choices=STATUS_ROOM_CHOICES,
        default='booked'
    )
    created_at = models.DateTimeField(
        'Дата создания бронирования',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

        constraints = [
            models.UniqueConstraint(
                fields=['room', 'check_in', 'check_out'],
                name='unique_booking_period',
                condition=models.Q(status__in=['booked', 'checked_in'])
            )
        ]

    @property
    def total_price(self):
        """Расчет стоймости проживантя"""
        if self.check_out <= self.check_in:
            return 0
        days = (self.check_out - self.check_in).days
        return days * self.room.price

    def clean(self):
        '''Валидация на уровне модели'''
        if not self.room.is_available:
            raise ValidationError(
                'Номер недоступен.'
            )
        if self.check_in < date.today():
            raise ValidationError(
                'Дата заезда не должна быть раньше текущей даты'
            )
        if self.check_out <= self.check_in:
            raise ValidationError(
                'Дата выселения должна быть позже даты заезда.'
            )
        if not self.room.is_available_for_period(
            self.check_in, self.check_out
        ):
            raise ValidationError('Номер уже забронирован на этот период.')
