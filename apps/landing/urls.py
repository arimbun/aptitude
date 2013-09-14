from django.conf.urls import url, patterns
from apps.landing import views

urlpatterns = patterns(
    '',
    # eg: /
    url(r'^$', views.index, name='index'),
    # eg: /book
    url(r'^blog', views.blog, name='book'),
    # eg: /book
    url(r'^book', views.book, name='book'),
    # eg: /confirm_booking
    url(r'^book/confirm', views.confirm_booking, name='book_confirm'),
    # eg: /book/failure
    url(r'^book/failure', views.book_failure, name='book_failure'),
    # eg: /book/success
    url(r'^book/success', views.book_success, name='book_success'),
    # eg: /consulting
    url(r'^consulting$', views.consulting, name='consulting'),
    # eg: /product
    url(r'^product$', views.product, name='product'),
    # eg: /solutions
    url(r'^solutions$', views.solutions, name='solutions'),
    # eg: /toc
    url(r'^toc', views.toc, name='toc'),
)