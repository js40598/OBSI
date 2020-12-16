from django.contrib import admin
from notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'reservation', 'user', 'datetime', 'is_viewed')
    list_display_links = ('title',)
    list_per_page = 50
    list_filter = ('reservation', 'user')


admin.site.register(Notification, NotificationAdmin)
