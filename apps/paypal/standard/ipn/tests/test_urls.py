from django.conf.urls.defaults import *

urlpatterns = patterns('apps.paypal.standard.ipn.views',
    (r'^ipn/$', 'ipn'),
)
