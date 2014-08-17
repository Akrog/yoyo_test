from django.conf.urls import patterns, url

from loyal.views import CustomerList, CustomerDetail

urlpatterns = patterns('',
                       url(r'^$', CustomerList.as_view(), name='customer-list'),
                       url(r'^(?P<pk>[0-9]+)$', CustomerDetail.as_view(), name='customer-detail'),
)
