from django.conf.urls import patterns, url, include

from loyal.views import CustomerListView, CustomerDetailView, StampList, VoucherListView, SaleListView

urlpatterns = patterns('',
                       url(r'^$', CustomerListView.as_view(), name='customer-list'),
                       url(r'^(?P<pk>[0-9]+)/?$', CustomerDetailView.as_view(), name='customer-detail'),
                       url(r'^(?P<pk>[0-9]+)/stamps/?$', StampList.as_view(), name='stamp-list'),
                       url(r'^(?P<pk>[0-9]+)/vouchers/?$', VoucherListView.as_view(), name='voucher-list'),
                       url(r'^(?P<pk>[0-9]+)/purchases/?$', SaleListView.as_view(), name='sale-list'),
)
