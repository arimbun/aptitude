from django.shortcuts import render_to_response
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _


def index(request):
    title = _('aptitude')
    keywords = 'aptitude, learning, child, brain'
    description = _('slogan')
    year = datetime.now().year
    return render_to_response('landing/index.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'year': year,
                              }
    )


def about_us(request):
    title = _('about us')
    return render_to_response('landing/about_us.html')

def solutions(request):
    title = _('solutions')
    return render_to_response('landing/solutions.html')

def product(request):
    title = _('solutions')
    return render_to_response('landing/product.html')