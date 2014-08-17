from django.conf.urls import patterns, url

from loyal.views import CustomerList

urlpatterns = patterns('',
                       url(r'^$', CustomerList.as_view(), name='customer-list'),
)
