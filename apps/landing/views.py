from apps.booking_types.models import BookingTypes
from apps.landing.models import Landing
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils.datetime_safe import datetime
from django import forms
import os

COMPANY_NAME = 'Aptitude World ANZ'
META_KEYWORDS = ['Aptitude World AU', 'Aptitude World NZ', 'Aptitude World Australia', 'Aptitude World New Zealand']


class PersonalForm(forms.Form):
    email_address = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=100)
    address = forms.CharField(max_length=150)
    suburb = forms.CharField(max_length=50)
    state = forms.ChoiceField(choices=[('NSW', 'New South Wales')])
    postcode = forms.CharField(max_length=4)
    # country = forms.ModelChoiceField(queryset=Country.objects.all())
    country = forms.ChoiceField(choices=[('Australia', 'Australia')])


class BookingForm(forms.Form):
    booking_type = forms.ModelChoiceField(queryset=BookingTypes.objects.all())
    appointment_date = forms.DateField(input_formats=['%d/%m/%Y'])
    message_to_our_consultant = forms.CharField(widget=forms.Textarea)


class PaymentForm(forms.Form):
    amount = forms.ChoiceField(
        choices=[('20 AUD', '20 AUD'), ('50 AUD', '50 AUD'), ('100 AUD', '100 AUD'), ('Full', 'Full')])


def index(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Home'
    return render_to_response('landing/index.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'index',
                                  'year': year,
                              }
    )


def product(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Product'
    return render_to_response('landing/product.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'product',
                                  'year': year,
                              }
    )


def solutions(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Solutions'
    return render_to_response('landing/solutions.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'solutions',
                                  'year': year,
                              }
    )


def consulting(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Consulting'
    return render_to_response('landing/consulting.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'consulting',
                                  'year': year,
                              }
    )


def book(request):
    personal_form = PersonalForm()
    booking_form = BookingForm()
    payment_form = PaymentForm()
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Book an Appointment'

    return render(request, 'landing/book.html',
                  {
                      'title': title,
                      'keywords': keywords,
                      'description': description,
                      'page': 'book',
                      'year': year,
                      'personal_form': personal_form,
                      'booking_form': booking_form,
                      'payment_form': payment_form,
                  }
    )


def confirm_booking(request):
    if request.method == 'POST':
        keywords, description, year = __init()
        title = COMPANY_NAME + ' - ' + 'Book an Appointment'
        environment = os.environ['ENVIRONMENT']
        # environment = 'production'

        personal_form = PersonalForm(request.POST)
        booking_form = BookingForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if personal_form.is_valid() and booking_form.is_valid() and payment_form.is_valid():
            # personal form data
            first_name = personal_form.cleaned_data['first_name']
            last_name = personal_form.cleaned_data['last_name']
            email_address = personal_form.cleaned_data['email_address']
            contact_number = personal_form.cleaned_data['contact_number']
            address = personal_form.cleaned_data['address']
            suburb = personal_form.cleaned_data['suburb']
            postcode = personal_form.cleaned_data['postcode']
            state = personal_form.cleaned_data['state']
            country = personal_form.cleaned_data['country']

            # booking form data
            booking_type = booking_form.cleaned_data['booking_type'].name
            appointment_date = booking_form.cleaned_data['appointment_date']
            message_to_our_consultant = booking_form.cleaned_data['message_to_our_consultant']

            # payment form data
            total_price_amount = int(booking_form.cleaned_data['booking_type'].price)
            total_price_currency = booking_form.cleaned_data['booking_type'].currency
            deposit_amount_raw = payment_form.cleaned_data['amount']

            # calculate deposit price
            if deposit_amount_raw == 'Full':
                deposit_price_amount = total_price_amount
                deposit_price_currency = total_price_currency
            else:
                deposit_amount_raw_array = deposit_amount_raw.split(' ')
                deposit_price_amount = int(deposit_amount_raw_array[0])
                deposit_price_currency = deposit_amount_raw_array[1]

            # calculate price left owing
            owing_amount = total_price_amount - deposit_price_amount
            owing_currency = total_price_currency

            total_price_str = str(total_price_amount) + ' ' + str(total_price_currency)
            deposit_paid_str = str(deposit_price_amount) + ' ' + str(deposit_price_currency)
            total_owing_str = str(owing_amount) + ' ' + str(owing_currency)

            return render(request, 'landing/confirm_booking.html',
                          {
                              'title': title,
                              'keywords': keywords,
                              'description': description,
                              'page': 'book',
                              'year': year,
                              'first_name': first_name,
                              'last_name': last_name,
                              'email_address': email_address,
                              'contact_number': contact_number,
                              'address': address,
                              'suburb': suburb,
                              'state': state,
                              'postcode': postcode,
                              'country': country,
                              'booking_type': booking_type,
                              'appointment_date': appointment_date,
                              'message_to_our_consultant': message_to_our_consultant,
                              'total_amount': total_price_str,
                              'deposit_amount': deposit_paid_str,
                              'owing_amount': total_owing_str,
                              'environment': environment,
                          }
            )
        else:
            return HttpResponseRedirect('/book')
    else:
        return HttpResponseRedirect('/book')


def email_confirmation(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            # get form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            booking_type = form.cleaned_data['booking_type'].name

            # calculate price
            total_price_amount = form.cleaned_data['booking_type'].price
            total_price_currency = form.cleaned_data['booking_type'].currency
            total_price_str = str(total_price_currency) + str(int(total_price_amount))
            deposit_paid_str = 'AUD5'
            total_owing_str = 'AUD30'

            # send confirmation email
            landing = Landing()
            reference_number = landing.generate_booking_reference_number(first_name, last_name)
            landing.send_confirmation_email(
                first_name=first_name,
                last_name=last_name,
                contact_number=form.cleaned_data['contact_number'],
                email_from='info@aptitudeworld.com.au',
                email_to=form.cleaned_data['email_address'],
                reference_number=reference_number,
                message=form.cleaned_data['message_to_our_consultant'],
                country=form.cleaned_data['country'],
                postcode=form.cleaned_data['postcode'],
                appointment_date=form.cleaned_data['appointment_date'],
                booking_type=booking_type,
                total_price=total_price_str,
                deposit_paid=deposit_paid_str,
                total_owing=total_owing_str)
            return HttpResponseRedirect('/book/success')
    else:
        return HttpResponseRedirect('/book/failure')


def book_success(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Booking Successful'
    return render_to_response('landing/book/success.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'book',
                                  'year': year,
                              }
    )


def book_failure(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Booking Failed'
    return render_to_response('landing/book/failure.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'book',
                                  'year': year,
                              }
    )


def __init():
    keywords = ','.join(META_KEYWORDS)
    description = ','.join(META_KEYWORDS)
    year = datetime.now().year
    return keywords, description, year