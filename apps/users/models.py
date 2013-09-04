from apps.countries.models import Country
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(models.Model):
    email_address = models.EmailField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    suburb = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=20)
    country = models.ForeignKey(Country, db_column='country_iso')
    receive_newsletter = models.BooleanField()
    administrator = models.BooleanField()
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(null=True)
    deleted = models.DateTimeField(null=True)


    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email_address
