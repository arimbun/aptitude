from django.conf.urls import url, patterns
from apps.landing import views

urlpatterns = patterns(
    '',
    # eg: /
    url(r'^$', views.index, name='index'),
    # eg: /book
    url(r'^blog$', views.blog, name='blog'),
    # # eg: /book
    # url(r'^book$', views.book, name='book'),
    # # eg: /book/confirm
    # url(r'^book/confirm$', views.confirm_booking, name='book_confirm'),
    # # eg: /book/failure
    # url(r'^book/failure$', views.book_failure, name='book_failure'),
    # # eg: /book/success
    # url(r'^book/success$', views.book_success, name='book_success'),
    # eg: /consulting
    url(r'^consulting$', views.consulting, name='consulting'),
    # eg: /product
    url(r'^product$', views.product, name='product'),
    # eg: /solutions
    url(r'^solutions$', views.solutions, name='solutions'),
    # eg: /toc
    url(r'^toc$', views.toc, name='toc'),
    # eg: /test_email
    url(r'^test_email$', views.test_email, name='test_email'),
    # eg: /contact
    url(r'^contact$', views.contact, name='contact'),
    # eg: /contact/submit
    url(r'^contact/submit$', views.submit_contact, name='contact_submit'),
    # eg: /contact/success
    url(r'^contact/success$', views.contact_success, name='contact_success'),
)