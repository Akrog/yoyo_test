from django.conf.urls import patterns, url, include

from loyal.views import StampListAllView, StampDetailView

urlpatterns = patterns('',
                       url(r'^$', StampListAllView.as_view(), name='stamp-list'),
                       url(r'^(?P<pk>[0-9]+)/?$', StampDetailView.as_view(), name='stamp-detail'),
)
