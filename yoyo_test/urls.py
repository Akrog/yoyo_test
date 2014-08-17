from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yoyo_test.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^/loyal/', include('loyal.urls', namespace='loyal')),
    url(r'^admin/', include(admin.site.urls)),
)
