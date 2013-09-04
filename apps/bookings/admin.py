from apps.bookings.models import Booking
from django.contrib import admin


class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'booking_type', 'email_address', 'paid_amount', 'appointment_date', 'created')
    list_filter = ['booking_type', 'created']


admin.site.register(Booking, BookingAdmin)