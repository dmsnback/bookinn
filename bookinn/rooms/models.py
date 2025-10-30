from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


ROOM_TYPE_CHOICES = (
    ('Standart', 'Стандарт'),
    ('Luxury', 'Люкс'),
    ('President', 'Президент'),
)


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
        choices=ROOM_TYPE_CHOICES,
        default='Standart'
    )
    description = models.TextField('Описание типа номера', blank=True)

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'
        unique_together = ('name',)

    def __str__(self):
        return self.get_name_display()


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
        decimal_places=2,
        null=True,
        blank=True
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

    def __str__(self):
        return f'{self.title} - {self.room_type}'


class Booking(models.Model):
    """Модель бронирования номера"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
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

    @property
    def total_price(self):
        """Расчет стоймости проживантя"""
        days = (self.check_out - self.check_in).days
        return days * self.room.price
