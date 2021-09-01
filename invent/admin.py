from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'tech_id', 'invent_id', 'time_create')
    list_display_links = ('id', 'tech_id')
    search_fields = ('title', 'tech_id', 'invent_id')
    list_filter = ('time_create', 'department', 'room')


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'department')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass
