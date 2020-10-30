from django.contrib import admin
from communicator.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'user', 'content', 'datetime')
    list_display_links = ('reservation', 'user')
    search_fields = ('reservation', 'user')
    list_per_page = 50
    list_editable = ('content', )
    list_filter = ('reservation', 'user')


admin.site.register(Message, MessageAdmin)
