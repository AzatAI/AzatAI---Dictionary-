from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UsersAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'phone_number')
    search_fields = ('email', 'first_name', 'last_name',)
    readonly_fields = ('id', 'password', 'is_admin', 'is_superuser', 'date_joined', 'last_login')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Users, UsersAdmin)

class DeviceAdmin(UserAdmin):

    list_display = ('device_id', 'user_id', 'device_os', 'ip', 'login_date')
    search_fields = ('ip',)
    readonly_fields = ('device_id', 'user_id', 'device_os', 'ip', 'login_date',)
    ordering = ('device_id',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Device,DeviceAdmin)