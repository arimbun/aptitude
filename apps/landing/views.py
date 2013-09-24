
import sys
sys.path.append('/opt/pycharm-2.7.3/helpers/pydev/')
import pydevd


from apps.blog.models import Post

from apps.booking_types.models import BookingTypes

from apps.landing.models import Landing
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils.datetime_safe import datetime
from django import forms


COMPANY_NAME = 'Aptitude World ANZ'
META_KEYWORDS = ['Aptitude World AU', 'Aptitude World NZ', 'Aptitude World Australia', 'Aptitude World New Zealand']


class BookingForm(forms.Form):
    # personal details section
    email_address = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=100)
    address = forms.CharField(max_length=150)
    suburb = forms.CharField(max_length=50)
    # state = forms.ChoiceField(choices=[('NSW', 'New South Wales')])
    postcode = forms.CharField(max_length=4)
    # country = forms.ModelChoiceField(queryset=Country.objects.all())
    # country = forms.ChoiceField(choices=[('Australia', 'Australia')])

    # booking details section
    booking_type = forms.ModelChoiceField(queryset=BookingTypes.objects.all())
    appointment_date = forms.DateField(input_formats=['%d/%m/%Y'])
    message_to_our_consultant = forms.CharField(widget=forms.Textarea, required=False,
                                                label="Message to our consultant (optional)")

    # payment details section
    amount = forms.ChoiceField(
        choices=[('50 AUD', 'AU$50'), ('Full', 'Full')])


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
    # pydevd.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
    booking_form = BookingForm()
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Book an Appointment'

    return render(request, 'landing/book.html',
                  {
                      'title': title,
                      'keywords': keywords,
                      'description': description,
                      'page': 'book',
                      'year': year,
                      'booking_form': booking_form,
                  }
    )


def confirm_booking(request):
    # pydevd.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
    if request.method == 'POST':
        keywords, description, year = __init()
        title = COMPANY_NAME + ' - ' + 'Confirm Booking'

        booking_form = BookingForm(request.POST)

        if booking_form.is_valid():
            # personal form data
            first_name = booking_form.cleaned_data['first_name']
            last_name = booking_form.cleaned_data['last_name']
            email_address = booking_form.cleaned_data['email_address']
            contact_number = booking_form.cleaned_data['contact_number']
            address = booking_form.cleaned_data['address']
            suburb = booking_form.cleaned_data['suburb']
            postcode = booking_form.cleaned_data['postcode']
            # state = booking_form.cleaned_data['state']
            # country = booking_form.cleaned_data['country']
            state = request.POST['state']
            country = request.POST['country']

            # booking form data
            booking_type = booking_form.cleaned_data['booking_type'].name
            appointment_date = datetime.strptime(request.POST['id_appointment_date_post'], '%Y-%m-%d')
            message_to_our_consultant = booking_form.cleaned_data['message_to_our_consultant']

            # payment form data
            total_price_amount = int(booking_form.cleaned_data['booking_type'].price)
            total_price_currency = booking_form.cleaned_data['booking_type'].currency
            deposit_amount_raw = booking_form.cleaned_data['amount']

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

            return render(request, 'landing/book/confirm.html',
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
                              'appointment_date': datetime.strftime(appointment_date, '%A, %d %B %Y'),
                              'message_to_our_consultant': message_to_our_consultant,
                              'total_amount': total_price_str,
                              'deposit_amount': deposit_paid_str,
                              'owing_amount': total_owing_str,
                          }
            )
        else:
            return render(request, 'landing/book.html',
                          {
                              'title': title,
                              'keywords': keywords,
                              'description': description,
                              'page': 'book',
                              'year': year,
                              'booking_form': booking_form,
                          })
    else:
        return HttpResponseRedirect('/book')


def book_success(request):
    if request.method == 'POST':
        # environment = os.environ['ENVIRONMENT']
        environment = 'production'
        # get form data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_address = request.POST['email_address']
        contact_number = request.POST['contact_number']
        address = request.POST['address']
        suburb = request.POST['suburb']
        state = request.POST['state']
        postcode = request.POST['postcode']
        country = request.POST['country']
        booking_type = request.POST['booking_type']
        appointment_date = request.POST['appointment_date']
        message_to_our_consultant = request.POST['message_to_our_consultant']
        total_amount = request.POST['total_amount']
        deposit_amount = request.POST['deposit_amount']
        owing_amount = request.POST['owing_amount']

        # send confirmation email
        landing = Landing()
        reference_number = landing.generate_booking_reference_number(first_name, last_name)
        landing.save_booking(
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            email_from='info@aptitudeworld.com.au',
            email_to=email_address,
            reference_number=reference_number,
            message=message_to_our_consultant,
            address=address,
            suburb=suburb,
            state=state,
            country=country,
            postcode=postcode,
            appointment_date=appointment_date,
            booking_type=booking_type,
            total_price=total_amount,
            deposit_paid=deposit_amount,
            total_owing=owing_amount)

        keywords, description, year = __init()
        title = COMPANY_NAME + ' - ' + 'Booking Successful'
        return render_to_response('landing/book/success.html',
                                  {
                                      'title': title,
                                      'keywords': keywords,
                                      'description': description,
                                      'booking_type': booking_type,
                                      'reference_number': reference_number,
                                      'deposit_amount': deposit_amount,
                                      'page': 'book',
                                      'year': year,
                                      'environment': environment,
                                  }
        )
    else:
        return HttpResponseRedirect('/book')


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


def toc(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Terms and Conditions'
    return render_to_response('landing/toc.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'toc',
                                  'year': year,
                              }
    )


def blog(request):
    keywords, description, year = __init()
    title = COMPANY_NAME + ' - ' + 'Blog'

    blog_posts = Post.objects.all()
    return render_to_response('landing/blog.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'blog',
                                  'year': year,
                                  'posts': blog_posts,
                              }
    )


def __init():
    keywords = ','.join(META_KEYWORDS)
    description = ','.join(META_KEYWORDS)
    year = datetime.now().year
    return keywords, description, year