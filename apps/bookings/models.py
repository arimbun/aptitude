from apps.booking_types.models import BookingTypes
from apps.users.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Booking(models.Model):
    reference_number = models.CharField(max_length=30)
    appointment_date = models.DateTimeField()
    message_to_consultant = models.TextField(null=True)
    paid_amount = models.FloatField()
    email_address = models.ForeignKey(User)
    booking_type = models.ForeignKey(BookingTypes)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(null=True)
    deleted = models.DateTimeField(null=True)


    # booking_package = None
    class Meta:
        db_table = 'bookings'
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')