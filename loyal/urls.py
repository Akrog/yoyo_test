from django.conf.urls import patterns, url, include

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from loyal.views import ProductListView, ProductDetailView

@api_view(('GET',))
def api_loyal(request, format=None):
    return Response({
        'customer': reverse('loyal:customer:customer-list', request=request, format=format),
        'products': reverse('loyal:product:product-list', request=request, format=format),
    })


urlpatterns = patterns('',
                       url(r'^$', api_loyal, name="root"),
                       url(r'^customer/', include('loyal.urls_customer', namespace='customer')),
                       url(r'^products/', include('loyal.urls_product', namespace='product')),
)
