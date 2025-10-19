from rest_framework import serializers

from rooms.models import Booking, Room, RoomType


class RoomTypeSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = RoomType
        fields = ('id', 'name', 'room_type_name', 'description')


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    room_type_id = serializers.PrimaryKeyRelatedField(
        queryset=RoomType.objects.all(),
        source='room',
        write_only=True
    )

    class Meta:
        model = Room
        fields = (
            'id',
            'title',
            'description',
            'room_type',
            'room_type_id',
            'is_avialible',
            'price',
            'capacity',
            'number_of_rooms'
        )


class BookingSerializer(serializers.ModelSerializer):

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
