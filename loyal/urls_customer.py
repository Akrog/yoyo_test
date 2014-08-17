from django.conf.urls import patterns, url, include

from loyal.views import CustomerList, CustomerDetail, StampList

urlpatterns = patterns('',
                       url(r'^$', CustomerList.as_view(), name='customer-list'),
                       url(r'^(?P<pk>[0-9]+)/?$', CustomerDetail.as_view(), name='customer-detail'),
                       url(r'^(?P<pk>[0-9]+)/stamps/?$', StampList.as_view(), name='stamp-list'),
)
