from django.contrib import admin
from .models import ServiceBooking, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'brand',
        'year',
        'price',
        'fuel_type',
        'color',
        'kilometers',
        'registration_number',
        'available',
    )
    list_filter = ('brand', 'fuel_type', 'available', 'year')
    search_fields = ('name', 'brand', 'registration_number', 'seller_name', 'seller_phone')
    list_editable = ('available', 'price')
    ordering = ('-id',)


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'car_model',
        'service_type',
        'preferred_date',
        'preferred_time',
        'phone',
        'status',
        'created_at',
    )
    list_filter = ('status', 'service_type', 'preferred_date')
    search_fields = ('customer_name', 'phone', 'car_model', 'registration_number')
    list_editable = ('status',)
    ordering = ('-created_at',)