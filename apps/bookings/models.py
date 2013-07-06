from django.db import models


class Booking(models.Model):
    reference_number = models.CharField(max_length=30)
    # booking_package = None