from django.conf.urls import patterns, url, include

from loyal.views import VoucherListAllView, VoucherDetailView

urlpatterns = patterns('',
                       url(r'^$', VoucherListAllView.as_view(), name='voucher-list'),
                       url(r'^(?P<pk>[0-9]+)/?$', VoucherDetailView.as_view(), name='voucher-detail'),
)
