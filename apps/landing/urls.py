from django.conf.urls import url, patterns
from apps.landing import views

urlpatterns = patterns(
    '',
    # eg: /
    url(r'^$', views.index, name='index'),
    # eg: /solutions
    url(r'^solutions$', views.solutions, name='solutions'),
    # eg: /product
    url(r'^product$', views.product, name='product'),
    # eg: /consulting
    url(r'^consulting$', views.consulting, name='consulting'),
    # eg: /book/success
    url(r'^book/success', views.book_success, name='book_success'),
    # eg: /book/failure
    url(r'^book/failure', views.book_failure, name='book_failure'),
    # eg: /confirm_booking
    url(r'^book/confirm', views.confirm_booking, name='confirm_booking'),
    # eg: /book
    url(r'^book', views.book, name='book'),
)