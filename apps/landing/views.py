from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _


def index(request):
    title = _('aptitude')
    keywords = 'aptitude, learning, child, brain'
    description = _('slogan')
    return render_to_response('landing/index.html',
                              {
                                  'title': title,
                                  'keywords': keywords,
                                  'description': description,
                              }
    )