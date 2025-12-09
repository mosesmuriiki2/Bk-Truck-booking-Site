from django.contrib import admin
from .models import Booking

@admin.action(description="Approve selected bookings")
def approve_bookings(modeladmin, request, queryset):
    queryset.update(status='approved')

@admin.action(description="Reject selected bookings")
def reject_bookings(modeladmin, request, queryset):
    queryset.update(status='rejected')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "truck", "customer_name", "start_date", "end_date", "status", "total_price")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("customer_name", "email", "phone")
    actions = [approve_bookings, reject_bookings]
