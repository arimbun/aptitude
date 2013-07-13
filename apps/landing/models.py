from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.db import models
from django.http import HttpResponse


class Landing(models.Model):
    def send_confirmation_email(self, first_name, last_name, contact_number, email_from, email_to, reference_number,
                                message, country, postcode, appointment_date, total_price, deposit_paid):
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
        Country: %s
        Postcode: %s
        Data scanning appointment: %s (A consultant will contact you to advise of the appointment time)
        Total Price: %s
        Deposit Paid: %s
        Total Owing: %s
        Message to consultant: %s

        Please find our booking terms & conditions below for your reference.

        -------------------

        Terms and Conditions:

        Payment of balance
        The outstanding balance is payable by the data scanning appointment time. We offer the following payment options:
        1. Payment by direct bank transfer (preferred)
            Account Name:               Aptitude World
            BSB:                        032 257
            Account number:             391306

            NOTE: Payments must include the booking reference number and surname
        2. Payment by cash at the data scanning appointment (please provide the exact amount)
        3. Payment by credit card via our website.

        Cancellation
        Should you have to cancel your assessment, you must notify us at least 24 hour in advance. The deposit is not refundable but transferrable once only. Once biometric data is taken, no cancellation of service can be made.

        Confidentiality
        Your personal data is treated with utmost privacy and confidentiality. Once the aptitude report is generated, the biometric data is automatically deleted from the system. We will not use any personal data without your prior consent.

        Disclaimer
        The undersigned has understood the nature of the service, agreed to subscribe to the said service and its consultation. Aptitude World does not make any representation, statement or remark to the undersigned on what the customer will or will not do based on the aptitude analysis. The analysis does not predict what the future holds. Aptitude World shall take its commitment in providing its service to the customer and no discrepancies shall be arised by either party after the consultation.

        -------------------

        Kind Regards,
        Aptitude World
        Ph 1300 88 78 71
        info@aptitudeworld.com.au
        """ % (
            reference_number, full_name, contact_number, ', '.join(email_to), country, postcode,
            self.format_date(appointment_date), self.format_price(total_price), self.format_price(deposit_paid),
            self.format_price(total_price - deposit_paid), message)

        try:
            send_mail(title, message, email_from, email_to, fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

    def generate_booking_reference_number(self, first_name, last_name):
        initials = str(first_name)[:1].upper() + str(last_name)[:1].upper()

        return 1

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