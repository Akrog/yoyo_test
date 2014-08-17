from django.conf.urls import patterns, url, include

from loyal.views import CustomerList, CustomerDetail, StampList

urlpatterns = patterns('',
                       url(r'^customer/', include('loyal.urls_customer', namespace='customer'))
)
