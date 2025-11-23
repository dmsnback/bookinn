from django.contrib import admin

from rooms.models import Booking, Room, RoomImage, RoomType


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ("image_tag", "image")
    readonly_fields = ("image_tag",)


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "room",
        "check_in",
        "check_out",
        "total_days_display",
        "total_price_display",
        "status",
        "created_at",
    )
    list_editable = ("check_in", "check_out", "status")
    search_fields = ("status", "room", "user")
    list_filter = ("status", "room", "user")
    list_display_links = ("room",)
    empty_value_display = "Не задано"

    def total_days_display(self, obj):
        return obj.total_days

    total_days_display.short_description = "Количество дней бронирования"

    def total_price_display(self, obj):
        return obj.total_price

    total_price_display.short_description = "Полная стоймость бронирования"


class RoomAdmin(admin.ModelAdmin):
    inlines = (RoomImageInline,)
    list_display = (
        "title",
        "room_type",
        "is_available",
        "price",
        "number_of_rooms",
        "capacity",
        "created_at",
    )
    list_editable = ("room_type", "is_available", "price")
    search_fields = (
        "title",
        "room_type",
        "is_available",
        "number_of_rooms",
        "capacity",
    )
    list_filter = (
        "title",
        "room_type",
        "price",
        "is_available",
        "number_of_rooms",
        "capacity",
    )
    list_display_links = ("title",)
    empty_value_display = "Не задано"


class RoomTypeAdmin(admin.ModelAdmin):
    inlines = (RoomInline,)
    list_display = ("name", "description")
    search_fields = ("name",)
    list_filter = ("name",)
    list_display_links = ("name",)
    empty_value_display = "Не задано"


class RoomImageAdmin(admin.ModelAdmin):
    list_display = ("room", "image_tag", "uploaded_at")
    search_fields = ("room", "image_tag")
    search_fields = ("room", "image_tag")
    list_filter = ("room",)
    list_display_links = ("room", "image_tag")
    empty_value_display = "Не задано"


admin.site.register(Booking, BookingAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(RoomImage, RoomImageAdmin)
