from django.shortcuts import render_to_response
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _


def index(request):
    title = _('aptitude')
    keywords = 'aptitude'
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


def product(request):
    title = _('product')
    keywords = 'aptitude'
    description = _('slogan')
    year = datetime.now().year
    return render_to_response('landing/product.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'year': year,
                              }
    )


def solutions(request):
    title = _('solutions')
    keywords = 'aptitude'
    description = _('slogan')
    year = datetime.now().year
    return render_to_response('landing/solutions.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'year': year,
                              }
    )


def consulting(request):
    title = _('consulting')
    keywords = 'aptitude'
    description = _('slogan')
    year = datetime.now().year
    return render_to_response('landing/consulting.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                                  'year': year,
                              }
    )