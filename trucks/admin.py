from django.contrib import admin
from django.utils.html import format_html
from .models import Truck, Driver, Extra

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "license_number", "active")
    search_fields = ("name", "license_number")
    list_filter = ("active",)
    readonly_fields = ("profile_picture_preview",)

    def profile_picture_preview(self, obj):
        if obj and obj.profile_picture:
            return format_html('<img src="{}" style="max-height:120px;" />', obj.profile_picture.url)
        return "No picture"
    profile_picture_preview.short_description = "Profile Picture"

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("name", "license_plate", "daily_price", "is_active", "driver")
    list_filter = ("is_active",)
    search_fields = ("name", "license_plate")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:120px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"

@admin.register(Extra)
class ExtraAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_per_day", "active")
    list_filter = ("category", "active")
    search_fields = ("name",)
