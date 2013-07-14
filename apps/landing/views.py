from apps.booking_types.models import BookingTypes
from apps.countries.models import Country
from apps.landing.models import Landing
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils.datetime_safe import datetime
from django import forms

COMPANY_NAME = 'Aptitude World ANZ'
META_KEYWORDS = ['Aptitude World AU', 'Aptitude World NZ', 'Aptitude World Australia', 'Aptitude World New Zealand']


class BookingForm(forms.Form):
    email_address = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=100)
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    postcode = forms.CharField(max_length=100)
    booking_type = forms.ModelChoiceField(queryset=BookingTypes.objects.all())
    appointment_date = forms.DateField(input_formats=['%d/%m/%Y'])
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
                message=form.cleaned_data['message'],
                country=form.cleaned_data['country'],
                postcode=form.cleaned_data['postcode'],
                appointment_date=form.cleaned_data['appointment_date'],
                booking_type=booking_type,
                total_price=total_price_str,
                deposit_paid=deposit_paid_str,
                total_owing=total_owing_str)
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


def __init():
    keywords = ','.join(META_KEYWORDS)
    description = ','.join(META_KEYWORDS)
    year = datetime.now().year
    return keywords, description, year