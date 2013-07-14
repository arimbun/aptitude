from django.conf.urls.defaults import *

urlpatterns = patterns('apps.paypal.standard.ipn.views',
    url(r'^$', 'ipn', name="paypal-ipn"),
)