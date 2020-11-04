from django.contrib import admin
from users.models import UserIncorrectLoginLimit

# Register your models here.


class UserIncorrectLoginLimitAdmin(admin.ModelAdmin):
    list_display = ('user', 'counter', 'is_blocked', 'blockade_expire')
    list_display_links = ('user', )
    search_fields = ('user', 'is_blocked')
    list_per_page = 50
    list_editable = ('counter', 'is_blocked')
    list_filter = ('is_blocked', )


admin.site.register(UserIncorrectLoginLimit, UserIncorrectLoginLimitAdmin)
