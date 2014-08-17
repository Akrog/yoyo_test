from django.conf.urls import patterns, url, include

from loyal.views import CustomerList, CustomerDetail, StampList, VoucherListView, SaleListView

urlpatterns = patterns('',
                       url(r'^$', CustomerList.as_view(), name='customer-list'),
                       url(r'^(?P<pk>[0-9]+)/?$', CustomerDetail.as_view(), name='customer-detail'),
                       url(r'^(?P<pk>[0-9]+)/stamps/?$', StampList.as_view(), name='stamp-list'),
                       url(r'^(?P<pk>[0-9]+)/vouchers/?$', VoucherListView.as_view(), name='voucher-list'),
                       url(r'^(?P<pk>[0-9]+)/purchases/?$', SaleListView.as_view(), name='sale-list'),
)
