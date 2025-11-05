from django.contrib import admin

from .models import Booking, Room, RoomType


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'room',
        'check_in',
        'check_out',
        'status',
        'created_at',
    )
    list_editable = (
        'check_in',
        'check_out',
        'status'
    )
    search_fields = (
        'status',
        'room',
        'user'
    )
    list_filter = (
        'status',
        'room',
        'user'
    )
    list_display_links = ('room',)
    empty_value_display = 'Не задано'


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'room_type',
        'is_available',
        'price',
        'number_of_rooms',
        'capacity',
        'created_at'
    )
    list_editable = (
        'room_type',
        'is_available',
        'price'
    )
    search_fields = (
        'title',
        'room_type',
        'is_available',
        'number_of_rooms',
        'capacity',
    )
    list_filter = (
        'title',
        'room_type',
        'is_available',
        'number_of_rooms',
        'capacity'
    )
    list_display_links = ('title',)
    empty_value_display = 'Не задано'


class RoomTypeAdmin(admin.ModelAdmin):
    inlines = (
        RoomInline,
    )
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    list_display_links = ('name',)
    empty_value_display = 'Не задано'


admin.site.register(Booking, BookingAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
