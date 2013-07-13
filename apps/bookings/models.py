from django.db import models
from django.utils.translation import ugettext_lazy as _


class Booking(models.Model):
    reference_number = models.CharField(max_length=30)
    # booking_package = None
    class Meta:
        db_table = 'bookings'
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')