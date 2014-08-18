from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from loyal.models import Product
from django.utils import timezone


class YoyoAPITestCase(APITestCase):
    """
    This class provides general methods needed to create API endpoint tests

    """

    CUST_LIST_ENDP  = 0
    CUST_DET_ENDP   = 1
    STAMP_LIST_ENDP = 2
    VOUCH_LIST_ENDP = 3
    SALE_LIST_ENDP  = 4
    VOUCHER_ENDP    = 5
    PRODUCT_ENDP    = 6
    STAMP_ENDP      = 7

    namespace_path = ['loyal', 'customer']


    endpoints = {
        CUST_LIST_ENDP  :'customer-list',
        CUST_DET_ENDP   :'customer-detail',
        STAMP_LIST_ENDP :'stamp-list',
        VOUCH_LIST_ENDP :'voucher-list',
        SALE_LIST_ENDP  :'sale-list',
        VOUCHER_ENDP    :'voucher:voucher-detail',
        PRODUCT_ENDP    :'product:product-detail',
        STAMP_ENDP      :'stamp:stamp-detail',
    }


    new_customer = {'first_name':"John",
                    'last_name':"Doe",
                    'email': "john.doe@gmail.com"}


    new_product = {
        'kind': Product.WIDGET,
        'date': timezone.now(),
        'serial_num': "1",
        'sale': None
    }

    URL_TEST_PREFIX = "http://testserver"


    def get_url(self, entrypoint, *args, **kwargs):
        namespace = ":".join(self.namespace_path)
        return reverse(namespace + ":" + self.endpoints[entrypoint], *args, **kwargs)

    def get_test_url(self, entrypoint, *args, **kwargs):
        return self.URL_TEST_PREFIX + self.get_url(entrypoint, *args, **kwargs)

    def get_non_customer_url(self, entrypoint, *args, **kwargs):
        return self.URL_TEST_PREFIX + reverse(self.namespace_path[0]+':'+self.endpoints[entrypoint], *args, **kwargs)
