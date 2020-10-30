from django.contrib import admin
from reservation.models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_begin', 'date', 'time', 'slug', 'is_upcoming')
    list_display_links = ('user', )
    search_fields = ('user', 'date')
    list_per_page = 8
    list_editable = ('date', 'time')
    list_filter = ('user', 'date', 'is_upcoming')
    readonly_fields = ('datetime_begin', 'slug', 'is_upcoming')


admin.site.register(Reservation, ReservationAdmin)
