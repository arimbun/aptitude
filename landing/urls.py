from django.conf.urls import url, patterns
from landing import views

urlpatterns = patterns('',
                       # eg: /
                       url(r'^$', views.index, name='index'),
)