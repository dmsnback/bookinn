from datetime import date

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from rooms.models import Booking, Room, RoomType


class RoomTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomType
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=RoomType.objects.all(),
                fields=('name'),
                message='Такой тип номера уже сущеествует.'
            )
        ]


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    room_type_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomType.objects.all(),
        source='room_type',
        write_only=True,
        help_text='Выберите тип номера'
    )

    class Meta:
        model = Room
        fields = (
            'id',
            'title',
            'description',
            'room_type',
            'room_type_id',
            'is_available',
            'price',
            'capacity',
            'number_of_rooms'
        )
        read_only_fields = ('id', 'is_available')
        validators = [
            UniqueTogetherValidator(
                queryset=Room.objects.all(),
                fields=('title', 'room_type'),
                message='Номер с таким названием уже существует'
            )
        ]

    def validate_prrice(self, value):
        '''Проверка, что цена за номер больше 0'''
        if value is not None and value <= 0:
            raise serializers.ValidationError('Цена должна быть больше 0')
        return value


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking
        fields = (
            'id',
            'user',
            'room',
            'check_in',
            'check_out',
            'status',
            'created_at'
        )
        read_only_fields = ('status', 'created_at')

    def validate(self, data):
        if data['check_in'] < date.today():
            raise serializers.ValidationError(
                'Дата заезда не должна быть раньше текущей даты'
            )
        if data['check_out'] < data['check_in']:
            raise serializers.ValidationError(
                'Дата выселения должна быть позже даты заезда.'
            )
        room = data['room']
        if room.is_available_for_period(data['check_in'], data['check_out']):
            raise serializers.ValidationError(
                'Номер уже забронирован на этот период'
            )
        return data

    def create(self, validated_data):
        validated_data['status'] = 'booked'
        return super().create(validated_data)
