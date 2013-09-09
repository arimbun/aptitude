from apps.booking_types.models import BookingTypes
from django.contrib import admin


class BookingTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')


admin.site.register(BookingTypes, BookingTypesAdmin)