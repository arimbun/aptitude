from django.conf.urls.defaults import *

urlpatterns = patterns('apps.paypal.standard.pdt.views',
    (r'^pdt/$', 'pdt'),
)
