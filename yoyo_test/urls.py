from django.conf.urls import patterns, include, url

from django.contrib import admin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'loyal': reverse('loyal:root', request=request, format=format),
        'admin': reverse('admin:index', request=request, format=format),
        'docs': reverse('django.swagger.base.view', request=request, format=format),
    })

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', api_root),
    url(r'^loyal/', include('loyal.urls', namespace='loyal')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
