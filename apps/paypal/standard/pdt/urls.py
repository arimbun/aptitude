from django.conf.urls.defaults import *

urlpatterns = patterns('apps.paypal.standard.pdt.views',
    url(r'^$', 'pdt', name="paypal-pdt"),
)