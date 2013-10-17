from datetime import datetime
from apps.booking_types.models import BookingTypes
from apps.bookings.models import Booking
from apps.countries.models import Country
from apps.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.db import models
import os


class Landing(models.Model):
    def save_booking(self, first_name, last_name, contact_number, email_from, email_to, reference_number,
                     message, address, suburb, state, country, postcode, appointment_date, total_price,
                     deposit_paid, total_owing, booking_type):
        """
        Saves the booking details into the database.
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
        :return: True if successful, False otherwise
        """
        appointment_date_obj = datetime.strptime(appointment_date, '%A, %d %B %Y')

        # if user exists, delete it
        try:
            existing_user = User.objects.get(email_address=email_to)
            if not existing_user.administrator:
                existing_user.first_name = first_name
                existing_user.last_name = last_name
                existing_user.contact_number = contact_number
                existing_user.address = address
                existing_user.suburb = suburb
                existing_user.state = state
                existing_user.postcode = country
                existing_user.country = Country.objects.get(iso='AU')
                existing_user.save()
        except ObjectDoesNotExist:
            pass

        # save user detail
        user = User(email_address=email_to, first_name=first_name, last_name=last_name, contact_number=contact_number,
                    address=address, suburb=suburb, state=state, postcode=postcode, receive_newsletter=True,
                    administrator=False, country=Country.objects.get(iso='AU'))
        user.save()

        # save booking detail
        deposit_paid_arr = deposit_paid.split(' ')
        deposit_paid_amount = float(deposit_paid_arr[0])
        booking = Booking(reference_number=reference_number, appointment_date=appointment_date_obj,
                          message_to_consultant=message, paid_amount=deposit_paid_amount, email_address=user,
                          booking_type=BookingTypes.objects.get(name=booking_type))
        booking.save()

        # send confirmation email to user
        self.send_confirmation_email(first_name, last_name, contact_number, email_from, email_to, reference_number,
                                     message, address, suburb, state, country, postcode, appointment_date,
                                     total_price, deposit_paid, total_owing, booking_type)

        return True

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
        :return: True if successful, False otherwise
        """
        title = 'Aptitude Assessment Booking Confirmation %s' % reference_number
        full_name = '%s %s' % (first_name, last_name)

        confirmation_email_html = open(os.getcwd() + '/apps/landing/templates/landing/email/confirmation_email.html',
                                       'r')
        email_html = confirmation_email_html.read() % (
            # reference_number, full_name, contact_number, email_to, address, suburb, state, postcode, country,
            # booking_type, appointment_date, total_price, deposit_paid, total_owing, message
            reference_number, full_name, contact_number, email_to, address, suburb, postcode,
            booking_type, appointment_date, total_price, deposit_paid, total_owing, message
        )

        confirmation_email_txt = open(os.getcwd() + '/apps/landing/templates/landing/email/confirmation_email.txt', 'r')
        email_txt = confirmation_email_txt.read() % (
            # reference_number, full_name, contact_number, email_to, address, suburb, state, postcode, country,
            # booking_type, appointment_date, total_price, deposit_paid, total_owing, message
            reference_number, full_name, contact_number, email_to, address, suburb, postcode,
            booking_type, appointment_date, total_price, deposit_paid, total_owing, message
        )

        try:
            email_message = EmailMultiAlternatives(title, email_txt, email_from, [email_to],
                                                   ['info@aptitudeworld.com.au'])
            # email_message = EmailMultiAlternatives(title, email_txt, email_from, [email_to])
            email_message.attach_alternative(email_html, 'text/html')
            email_message.send()

            return True
        except BadHeaderError:
            # return HttpResponse('Invalid header found.')
            return False
        finally:
            return True

    def send_contact_email(self, first_name, last_name, contact_number, email_from, email_to, message):
        full_name = '%s %s' % (first_name, last_name)
        title = 'Expression of Interest - %s' % full_name
        confirmation_email_txt = open(os.getcwd() + '/apps/landing/templates/landing/email/contact_email.txt', 'r')
        email_txt = confirmation_email_txt.read() % (
            full_name, email_to, contact_number, message
        )

        try:
            email_message = EmailMultiAlternatives(title, email_txt, email_from, ['info@aptitudeworld.com.au'])
            # email_message = EmailMultiAlternatives(title, email_txt, email_from, [email_to])
            email_message.send()

            return True
        except BadHeaderError:
            # return HttpResponse('Invalid header found.')
            return False
        finally:
            return True

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