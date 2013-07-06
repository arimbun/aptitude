from django.core.mail import send_mail, BadHeaderError
from django.db import models
from django.http import HttpResponse


class Landing(models.Model):
    def send_confirmation_email(first_name, last_name, contact_number, email_from, email_to, reference_number):
        """
        Sends a booking confirmation email to the customer.
        :param first_name: Customer's first name
        :param last_name: Customer's last name
        :param contact_number: Customer's contact number
        :param email_from: Email FROM
        :param email_to: EMAIL TO
        :param reference_number: Booking reference number
        :return:
        """
        title = 'Aptitude Assessment Booking Confirmation %s' % reference_number
        full_name = '%s %s' % (first_name, last_name)
        message = """
        Thank you for booking your aptitude assessment online. We look forward to helping you unveil your potentials. Below are the details for your booking.

        Booking reference number: %s
        Name: %s
        Contact Number: %s
        Email Address: %s
        Data scanning appointment: %s
        Total Price: %s
        Deposit Paid: %s
        Total Owing: %s

        Please find attached our booking terms & conditions for your reference.

        Kind Regards,
        Aptitude World
        Ph 1300 88 78 71
        info@aptitudeworld.com.au
        """ % (reference_number, full_name, contact_number, email_to, 'Saturday 6 April 2013, 1:00 PM', '$275 inc GST',
               '$100', '$175')

        try:
            send_mail(title, message, email_from, email_to, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')