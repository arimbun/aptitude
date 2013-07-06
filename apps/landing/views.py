import sys
from apps.countries.models import Country
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.utils.datetime_safe import datetime
from django import forms

COMPANY_NAME = 'Aptitude World ANZ'
META_KEYWORDS = ['Aptitude World AU', 'Aptitude World NZ', 'Aptitude World Australia', 'Aptitude World New Zealand']


class BookingForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=100)
    email = forms.EmailField()
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    postcode = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


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
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # reference_number = request.POST.get('reference')
            reference_number = '123'
            send_confirmation_email(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                contact_number=request.POST.get('contact_number'),
                email_from='info@aptitudeworld.com.au',
                email_to=[request.POST.get('email')],
                reference_number=reference_number)
            return HttpResponseRedirect('/')
    else:
        form = BookingForm()

    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Book an Appointment'
    return render(request, 'landing/book.html',
                  {
                      'title': title,
                      'keywords': keywords,
                      'description': description,
                      'page': 'book',
                      'year': year,
                      'form': form,
                  }
    )


def send_confirmation_email(first_name, last_name, contact_number, email_from, email_to, reference_number):
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


def __init():
    keywords = ','.join(META_KEYWORDS)
    description = ','.join(META_KEYWORDS)
    year = datetime.now().year
    return keywords, description, year