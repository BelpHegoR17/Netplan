from django.contrib import admin
from .models import Device
# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name","device_type","ip_address","status","location","added_on")
    search_fields=("name","ip_address","mac_address")
    list_filter=("status","device_type")