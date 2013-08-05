from django.db import models
from django.utils.translation import ugettext_lazy as _


class BookingTypes(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    currency = models.CharField(max_length=3)

    class Meta:
        db_table = 'booking_types'
        verbose_name = _('BookingType')
        verbose_name_plural = _('BookingTypes')

    def __unicode__(self):
        return self.name + ' (' + str(int(self.price)) + ' ' + self.currency + ')'

        # def get_name(self):
        #     return self.name
        #
        # def get_price(self):
        #     return self.price