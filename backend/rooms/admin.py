from django.contrib import admin
from rooms.models import Floor, Room, AdditionalEquipment


class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'level')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('floor', 'sign', 'destination', 'number_of_places', 'availability_level')
    list_display_links = ('floor', )
    search_fields = ('destination', 'floor', 'availability_level')
    list_per_page = 50
    list_editable = ('destination', 'number_of_places', 'availability_level')
    list_filter = ('destination', 'floor')
    readonly_fields = ('room_slug', )


class AdditionalEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(Floor, FloorAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(AdditionalEquipment, AdditionalEquipmentAdmin)
