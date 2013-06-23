from django.conf.urls import url, patterns
from apps.landing import views

urlpatterns = patterns('',
                       # eg: /
                       url(r'^$', views.index, name='index'),
                       # eg: /solutions
                       url(r'^solutions$', views.solutions, name='solutions'),
                       # eg: /product
                       url(r'^product$', views.product, name='product'),
                       # eg: /consulting
                       url(r'^consulting$', views.consulting, name='consulting'),
)