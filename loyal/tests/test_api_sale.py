from rest_framework import status
from loyal.models import Customer, Product, Sale, Stamp, Voucher
from .yoyo_api_testcase import YoyoAPITestCase

from django.utils import timezone
from datetime import datetime

import names as gen_names



class APISale(YoyoAPITestCase):
    """
    This class tests following endpoints
        /loyal/customer/sales
    """


    def test_sales_list_empty(self):
        """
        Test that for a given customer initially the sales list is empty.
        This tests the GET endpoint /loyal/customer/${id}/sales
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.SALE_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_sales_list_populated(self):
        """
        Test that for a given customer we can see it's purchases.
        We create 2 sales directly in the DB, one without products the other with 1 product
        This tests the GET from endpoint /loyal/customer/${id}/sales
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Create sales
        s = Sale(customer=c, date=timezone.now())
        s.save()

        s = Sale(customer=c, date=timezone.now())
        s.save()

        # Create product
        new_product = dict(self.new_product)
        new_product['sale'] = s
        p = Product(**new_product)
        p.save()

        # Get list
        url = self.get_url(self.SALE_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

        sale_data = {"date": response.data[0].get("date", None), 'products':[]}
        self.assertEqual(response.data[0], sale_data)

        sale_data = {"date": response.data[1].get("date", None), 'products':[str(p)]}
        self.assertEqual(response.data[1], sale_data)


    def test_create_sale_with_no_date(self):
        """
        Test that creates a sale without a date
        This tests the POST from endpoint /loyal/customer/${id}/sales
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create  through API
        url = self.get_url(self.SALE_LIST_ENDP, args=[c.pk])
        response = self.client.post(url)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_sale(self):
        """
        Test that creates a single sale with no product
        This tests the POST from endpoint /loyal/customer/${id}/sales
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create  through API
        my_time = timezone.now()

        url = self.get_url(self.SALE_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, {'date':str(my_time)})

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'date':my_time, 'products':[]})


    def test_create_sale_non_existan_owner(self):
        """
        Test that tries to create a sale with an unkown owner
        This tests the POST from endpoint /loyal/customer/${id}/sales
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create  through API
        url = self.get_url(self.SALE_LIST_ENDP, args=[c.pk+1])
        response = self.client.post(url, {'date':timezone.now()})

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
