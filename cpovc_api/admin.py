from django.contrib import admin
from .models import DeviceManagement


class DeviceManagementAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'user', 'is_blocked', 'is_void',
                    'timestamp_created', 'timestamp_updated')
    search_fields = ('device_id', 'timestamp_created')

    list_filter = ['is_blocked', 'is_void']


admin.site.register(DeviceManagement, DeviceManagementAdmin)
