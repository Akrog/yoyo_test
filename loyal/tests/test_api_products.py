from rest_framework import status
from loyal.models import Customer, Product, Sale, Stamp, Voucher
from rest_framework.test import APITestCase

from django.utils import timezone
from datetime import datetime

from django.core.urlresolvers import reverse
from loyal.serializers import ProductSerializer


class APIProduct(APITestCase):
    """
    This class tests following endpoints
        /loyal/products
    """

    ENDPOINT = reverse('loyal:product-list')

    EMPTY_LIST = {
        'count': 0,
        'next': None,
        'previous': None,
        'results': []
    }

    new_product = {
        'kind': Product.WIDGET,
        'date': timezone.now(),
        'serial_num': "1",
        'sale': None
    }


    def test_product_list_empty(self):
        """
        Test that initially we don't have any products
        This tests the GET endpoint /loyal/products
        """

        # Get list
        response = self.client.get(self.ENDPOINT)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.EMPTY_LIST)



    def test_sales_list_populated(self):
        """
        Test that we can retrieve products from the DB using the endpoint.
        We create 2 products directly in the DB
        This tests the GET from endpoint /loyal/products
        """

        # Create product
        new_product = dict(self.new_product)
        expected_response = dict(self.EMPTY_LIST)

        p = Product(**new_product)
        p.save()
        products = [p]

        new_product['serial_num'] = str(1+int(new_product['serial_num']))
        p = Product(**new_product)
        p.save()
        products.append(p)

        expected_response['results'] = ProductSerializer(products, many=True).data
        expected_response['count'] = 2

        # Get list
        response = self.client.get(self.ENDPOINT)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data['results']))

        self.assertEqual(response.data, expected_response)


    def test_create_product(self):
        """
        Test that creates a single product
        This tests the POST from endpoint /loyal/products
        """
        my_time = datetime.now()

        # Create  through API
        new_product = dict(self.new_product)
        new_product['date'] = str(my_time)

        response = self.client.post(self.ENDPOINT, new_product)

        # Confirm it's OK
        new_product['date'] = my_time
        new_product['kind_name'] = Product.PRODUCT_CHOICES[new_product['kind']][1]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, new_product)


    def test_create_product_repeat_serial(self):
        """
        Test that tries to create a product with a repeated serial number
        This tests the POST from endpoint /loyal/products
        """

        p = Product(**self.new_product)
        p.save()

        # Create  through API
        response = self.client.post(self.ENDPOINT, self.new_product)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_product_wrong_kind(self):
        """
        Test that tries to create a product with an incorrect king
        This tests the POST from endpoint /loyal/products
        """

        new_product = dict(self.new_product)
        new_product['kind'] = len(Product.PRODUCT_CHOICES)

        # Create  through API
        response = self.client.post(self.ENDPOINT, new_product)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_product_empty_serial(self):
        """
        Test that tries to create a product with an empty serial number
        This tests the POST from endpoint /loyal/products
        """

        new_product = dict(self.new_product)
        new_product['serial_num'] = ""

        # Create  through API
        response = self.client.post(self.ENDPOINT, new_product)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_product_wrong_sale(self):
        """
        Test that tries to create a product with a non existant sale
        This tests the POST from endpoint /loyal/products
        """

        new_product = dict(self.new_product)
        new_product['sale'] = 1

        # Create  through API
        response = self.client.post(self.ENDPOINT, new_product)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_product_wrong_date(self):
        """
        Test that tries to create a product with a wrongly formated date
        This tests the POST from endpoint /loyal/products
        """

        new_product = dict(self.new_product)
        new_product['date'] = "17 march 2015"

        # Create  through API
        response = self.client.post(self.ENDPOINT, new_product)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
