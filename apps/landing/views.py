from apps.countries.models import Country
from apps.landing.models import Landing
from django.http import HttpResponseRedirect
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
            Landing.send_confirmation_email(
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


def __init():
    keywords = ','.join(META_KEYWORDS)
    description = ','.join(META_KEYWORDS)
    year = datetime.now().year
    return keywords, description, year