#sys.path.append('/opt/pycharm-2.7.3/helpers/pydev/')
#import pydevd


from apps.blog.models import Post

from apps.booking_types.models import BookingTypes

from apps.landing.models import Landing
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils.datetime_safe import datetime
from django import forms


COMPANY_NAME = 'Aptitude World'
META_KEYWORDS = ['Aptitude World', 'Aptitude World ANZ', 'Aptitude World AU', 'Aptitude World NZ',
                 'Aptitude World Australia', 'Aptitude World New Zealand']


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
    booking_type = forms.ModelChoiceField(queryset=BookingTypes.objects.order_by('name'))
    appointment_date = forms.DateField(input_formats=['%d/%m/%Y'])
    message_to_our_consultant = forms.CharField(widget=forms.Textarea, required=False,
                                                label="Message to our consultant (optional)")

    # payment details section
    amount = forms.ChoiceField(
        choices=[('50 AUD', 'AU$50'), ('Full', 'Full')])


class ContactForm(forms.Form):
    email_address = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=100)
    message_to_our_consultant = forms.CharField(widget=forms.Textarea, label="Message")


def index(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Home'
    description = 'Aptitude World helps children and adults to unleash their potential with proven scientific methodology.'
    return render_to_response('landing/index.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'index',
                                  'year': year,
                              }
    )


def dermatoglyphics(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Product'
    description = 'The study of Dermatoglyphics (dermato=skin, glyphics=carvings) can be traced back to almost 200 years of research. This study has been proven with evidence in anthropology, genetics, neuroscience and statistics to decode human\'s innate ability (inborn characteristic).'
    return render_to_response('landing/dermatoglyphics.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'dermatoglyphics',
                                  'year': year,
                              }
    )


def consulting(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Consulting'
    description = 'Aptitude World has a 3-Way Approach to discover the innate abilities and talent of an individual as illustrated in the below image.'
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
    keywords, year = __init()
    description = 'To book an appointment with one of our consultants, please fill in the form below.'
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


def contact(request):
    contact_form = ContactForm()
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Contact Us'
    description = 'Give us a ring. We would love to chat with you.'

    return render(request, 'landing/contact/index.html',
                  {
                      'title': title,
                      'keywords': keywords,
                      'description': description,
                      'page': 'contact',
                      'year': year,
                      'contact_form': contact_form,
                  }
    )


def contact_success(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Contact Us'
    description = 'Give us a ring. We would love to chat with you.'

    return render(request, 'landing/contact/success.html',
                  {
                      'title': title,
                      'keywords': keywords,
                      'description': description,
                      'page': 'contact',
                      'year': year,
                  }
    )


def submit_contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # personal form data
            first_name = contact_form.cleaned_data['first_name']
            last_name = contact_form.cleaned_data['last_name']
            email_address = contact_form.cleaned_data['email_address']
            contact_number = contact_form.cleaned_data['contact_number']
            message_to_our_consultant = contact_form.cleaned_data['message_to_our_consultant']

            landing = Landing()
            landing.send_contact_email(
                first_name=first_name,
                last_name=last_name,
                contact_number=contact_number,
                email_from='info@aptitudeworld.com.au',
                email_to=email_address,
                message=message_to_our_consultant)

            return HttpResponseRedirect('/contact/success')
        else:
            return HttpResponseRedirect('/contact')
    else:
        return HttpResponseRedirect('/contact')


def confirm_booking(request):
    # pydevd.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
    if request.method == 'POST':
        keywords, year = __init()
        description = 'Please review your order below'
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

        keywords, year = __init()
        description = ''
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
    keywords, year = __init()
    description = ''
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
    keywords, year = __init()
    description = ''
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
    keywords, year = __init()
    description = ''
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


def testimonials(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Testimonials'
    description = 'Here are a few lines that our happy customers have come back with and say about our services.'

    return render_to_response('landing/testimonials.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'testimonials',
                                  'year': year,
                              }
    )


def franchising(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Franchising'
    description = 'Join the global Aptitude World family! We welcome your interest for a franchise opportunity.'

    return render_to_response('landing/franchising.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'franchising',
                                  'year': year,
                              }
    )


def faq(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'FAQ'
    description = 'Your Frequently Asked Questions answered.'

    return render_to_response('landing/faq.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'faq',
                                  'year': year,
                              }
    )


def report_content(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Report Content'
    description = ''

    return render_to_response('landing/report_content.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'report_content',
                                  'year': year,
                              }
    )


def gallery(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'Gallery'
    description = ''

    return render_to_response('landing/gallery.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'gallery',
                                  'year': year,
                              }
    )


def about_us(request):
    keywords, year = __init()
    title = COMPANY_NAME + ' - ' + 'About Us'
    description = 'Aptitude World is a group of dynamic professionals coming from various fields whom being parents ourselves, are passionate about children development and believe in utilising modern technology to assist us in guiding our children to the best that they can be.'

    return render_to_response('landing/about_us.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'page': 'about_us',
                                  'year': year,
                              }
    )


def test_email(request):
    landing = Landing()
    landing.send_confirmation_email('arthur', 'rimbun', '0413751601', 'anggiarto@gmail.com', 'anggiarto@gmail.com',
                                    'FA123', 'message', 'address', 'suburb', 'state', 'country', 'postcode',
                                    'appointment date', '$500', '$100', '$400', 'booking type')


def __init():
    keywords = ','.join(META_KEYWORDS)
    year = datetime.now().year
    return keywords, year
