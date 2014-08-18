from django.conf.urls import patterns, url, include

from loyal.views import ProductListView, ProductDetailView

urlpatterns = patterns('',
                       url(r'^$', ProductListView.as_view(), name='product-list'),
                       url(r'^(?P<pk>[0-9]+)/?$', ProductDetailView.as_view(), name='product-detail'),
)
