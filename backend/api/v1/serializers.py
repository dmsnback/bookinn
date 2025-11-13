from datetime import date

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from rooms.models import Booking, Room, RoomImage, RoomType


class RoomTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomType
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=RoomType.objects.all(),
                fields=('name',),
                message='Такой тип номера уже сущеествует.'
            )
        ]


class RoomImageReadSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RoomImage
        fields = ('room', 'image')
        read_only_fields = ('id',)


class RoomImageWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomImage
        fields = ('id', 'room', 'image', 'uploaded_at')
        read_only_fields = ('id', 'uploaded_at')


class RoomReadSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    images = RoomImageReadSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            'id',
            'title',
            'description',
            'room_type',
            'is_available',
            'price',
            'capacity',
            'number_of_rooms',
            'images'
        )


class RoomWriteSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    room_type_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomType.objects.all(),
        source='room_type',
        write_only=True,
        help_text='Выберите тип номера'
    )
    image = serializers.ImageField(
        write_only=True,
        required=False,
        help_text='Добавьте фото для номеера'
    )
    images = RoomImageWriteSerializer(many=True, read_only=True)
    is_available = serializers.BooleanField(default=True)

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
            'number_of_rooms',
            'image',
            'images',
        )
        read_only_fields = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=Room.objects.all(),
                fields=('title', 'room_type'),
                message='Номер с таким названием уже существует'
            )
        ]

    def validate_price(self, value):
        '''Проверка, что цена за номер больше 0'''
        if value is not None and value <= 0:
            raise serializers.ValidationError('Цена должна быть больше 0')
        return value

    def create(self, validated_data):
        if 'image' not in self.initial_data:
            room = Room.objects.create(**validated_data)
            return room
        image = validated_data.pop('image', None)
        room = Room.objects.create(**validated_data)
        if image:
            RoomImage.objects.create(room=room, image=image)
        return room

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image:
            RoomImage.objects.create(room=instance, image=image)
        return instance


class BookingReadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    room = serializers.StringRelatedField(read_only=True)
    total_days = serializers.StringRelatedField(read_only=True)
    total_price = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'user',
            'room',
            'check_in',
            'check_out',
            'total_days',
            'total_price',
            'status',
            'created_at'
        )


class BookingWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    total_days = serializers.StringRelatedField(read_only=True)
    total_price = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id',
            'user',
            'room',
            'check_in',
            'check_out',
            'total_days',
            'total_price',
            'status',
            'created_at'
        )
        read_only_fields = ('id', 'created_at', 'total_days', 'total_price')

    def validate(self, data):
        check_in = data.get(
            'check_in',
            getattr(self.instance, 'check_in', None)
        )
        check_out = data.get(
            'check_out',
            getattr(self.instance, 'check_out', None)
        )
        room = data.get('room', getattr(self.instance, 'room', None))
        if check_in < date.today():
            raise serializers.ValidationError(
                'Дата заезда не должна быть раньше текущей даты'
            )
        if check_out < check_in:
            raise serializers.ValidationError(
                'Дата выселения должна быть позже даты заезда.'
            )
        if not room.is_available:
            raise serializers.ValidationError('Номер не доступен')
        if not room.is_available_for_period(
            check_in,
            check_out,
            exclude_booking=self.instance
        ):
            raise serializers.ValidationError(
                'Номер уже забронирован на этот период'
            )
        return data

    def create(self, validated_data):
        validated_data['status'] = 'booked'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        '''При PATCH обязательно передать status, проблема пока не решена'''

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
