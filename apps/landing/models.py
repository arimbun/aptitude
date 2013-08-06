from datetime import datetime
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
from django.http import HttpResponse
import os


class Landing(models.Model):
    def send_confirmation_email(self, first_name, last_name, contact_number, email_from, email_to, reference_number,
                                message, address, suburb, state, country, postcode, appointment_date, total_price,
                                deposit_paid, total_owing, booking_type):
        """
        Sends a booking confirmation email to the customer.

        :param first_name:
        :param last_name:
        :param contact_number:
        :param email_from:
        :param email_to:
        :param reference_number:
        :param message:
        :param address:
        :param suburb:
        :param state:
        :param country:
        :param postcode:
        :param appointment_date:
        :param total_price:
        :param deposit_paid:
        :param total_owing:
        :param booking_type:
        :return:
        """
        title = 'Aptitude Assessment Booking Confirmation %s' % reference_number
        full_name = '%s %s' % (first_name, last_name)

        confirmation_email_html = open(os.getcwd() + '/apps/landing/templates/landing/confirmation_email.html', 'r')
        email_html = confirmation_email_html.read() % (
            reference_number, full_name, contact_number, email_to, address, suburb, state, country, postcode,
            booking_type, appointment_date, total_price, deposit_paid, total_owing, message
        )

        confirmation_email_txt = open(os.getcwd() + '/apps/landing/templates/landing/confirmation_email.txt', 'r')
        email_txt = confirmation_email_txt.read() % (
            reference_number, full_name, contact_number, email_to, address, suburb, state, country, postcode,
            booking_type, appointment_date, total_price, deposit_paid, total_owing, message
        )

        try:
            email_message = EmailMultiAlternatives(title, email_txt, email_from,
                                                   [email_to, 'info@aptitudeworld.com.au'])
            email_message.attach_alternative(email_html, 'text/html')
            email_message.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

    def generate_booking_reference_number(self, first_name, last_name):
        initials = first_name[:1].upper() + last_name[:1].upper()
        dateobj = datetime.now()
        year = dateobj.year - 2012
        reference_number = str(initials) + str(year) + str(dateobj.hour) + str(dateobj.minute) + str(dateobj.second)
        return reference_number

    def format_date(self, date):
        # parse date
        # day, month, year = self.__parse_date(date)
        # dateobj = datetime(year, month, day)
        return date.strftime('%A, %d %B %Y')

    def format_price(self, price):
        return str(price) + ' inc. GST'

    def __parse_date(self, date):
        date_arr = date.split('/')
        day = date_arr[0]
        month = date_arr[1]
        year = date_arr[2]
        return day, month, year