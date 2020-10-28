from django.contrib import admin
from pages.models import Floor, Room, Reservation, Message

# Register your models here.


class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('floor', 'sign', 'destination', 'number_of_places', 'availability_level')
    list_display_links = ('floor', )
    search_fields = ('destination', 'floor', 'availability_level')
    list_per_page = 50
    list_editable = ('destination', 'number_of_places', 'availability_level')
    list_filter = ('destination', 'floor')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_begin', 'date', 'time', 'slug', 'is_upcoming')
    list_display_links = ('user', )
    search_fields = ('user', 'date')
    list_per_page = 8
    list_editable = ('date', 'time')
    list_filter = ('user', 'date', 'is_upcoming')
    readonly_fields = ('datetime_begin', 'slug', 'is_upcoming')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'user', 'content', 'datetime')
    list_display_links = ('reservation', 'user')
    search_fields = ('reservation', 'user')
    list_per_page = 50
    list_editable = ('content', )
    list_filter = ('reservation', 'user')


admin.site.register(Floor, FloorAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Message, MessageAdmin)
