from rest_framework import status
from django.core.urlresolvers import reverse
from django.utils import timezone

from loyal.models import Customer, Product, Sale, Stamp, Voucher
from loyal.serializers import CustomerSerializerList
from .yoyo_api_testcase import YoyoAPITestCase

import names as gen_names



class APICustomer(YoyoAPITestCase):
    """
    This class tests following endpoints
        /loyal/customer
    """


    def test_get_list_empty(self):
        """
        Test that endpoint's GET for customers list is working.
        On an empty DB it should always return empty list.
        This tests the GET endpoint /loyal/customer
        """

        # Get list
        url = self.get_url(self.CUST_LIST_ENDP)
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])



    def test_get_list_one_customer(self):
        """
        Verify that the customers list endpoint returns customers from the DB.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.CUST_LIST_ENDP)
        response = self.client.get(url)

        # Create expected customer, now includes the id
        expected_customer = dict(self.new_customer)
        expected_customer.update({
            'id': c.pk,
            'details': self.get_test_url(self.CUST_DET_ENDP, args=[c.pk])
        })

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqual(expected_customer, response.data[0])


    def test_get_list_20_customers(self):
        """
        Verify that the customers list endpoint returns customers from the DB.
        This is a more advanced test with 20 different customers.
        This tests the GET endpoint /loyal/customer
        """

        # Create customers
        customers = []
        for _ in xrange(20):
            name = gen_names.get_first_name()
            surname = gen_names.get_last_name()
            customer = Customer(first_name=name, last_name=surname, email=name+"@"+surname+".com")
            customer.save()
            customers.append(customer)

        # Transform customers
        expected_response = CustomerSerializerList(customers, many=True).data
        for customer in expected_response:
            customer['details'] = self.URL_TEST_PREFIX + customer['details']

        # Get list from endpoint
        url = self.get_url(self.CUST_LIST_ENDP)
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(20, len(response.data))
        self.assertEqual(expected_response, response.data)


    def test_list_create_one_customer(self):
        """
        Verify that the customers list endpoint works for customer creation.
        Simple test that will POST only 1 new customer
        This tests the POST endpoint /loyal/customer
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        response = self.client.post(url, self.new_customer)

        # Create expected customer, now includes the id
        expected_customer = dict(self.new_customer)
        expected_customer.update({
            'id': 1,
            'details': self.get_test_url(self.CUST_DET_ENDP, args=[1])
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_customer)


    def test_list_create_customer_empty_name(self):
        """
        Verify that the customers detail endpoint doesn't accept empty name.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        my_customer = dict(self.new_customer)
        my_customer['first_name'] = ""
        response = self.client.post(url, my_customer)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_create_customer_without_name(self):
        """
        Verify that the customers detail endpoint doesn't accept a request with the name missing.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        my_customer = dict(self.new_customer)
        del my_customer['first_name']
        response = self.client.post(url, my_customer)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_create_customer_empty_surname(self):
        """
        Verify that the customers detail endpoint doesn't accept empty last name.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        my_customer = dict(self.new_customer)
        my_customer['last_name'] = ""
        response = self.client.post(url, my_customer)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_create_customer_without_surname(self):
        """
        Verify that the customers detail endpoint doesn't accept a request with the last name missing.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        my_customer = dict(self.new_customer)
        del my_customer['last_name']
        response = self.client.post(url, my_customer)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_create_customer_empty_email(self):
        """
        Verify that the customers detail endpoint doesn't accept empty email.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        my_customer = dict(self.new_customer)
        my_customer['email'] = ""
        response = self.client.post(url, my_customer)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_create_customer_without_email(self):
        """
        Verify that the customers detail endpoint doesn't accept a request with the email missing.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        my_customer = dict(self.new_customer)
        del my_customer['email']
        response = self.client.post(url, my_customer)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_list_create_20_customer(self):
        """
        Verify that the customers list endpoint works for customer creation.
        More advanced test that will POST only 20 new customer
        This tests the POST endpoint /loyal/customer
        """

        created_customers = []
        # POST creation
        url = self.get_url(self.CUST_LIST_ENDP)
        for i in xrange(20):
            name = gen_names.get_first_name()
            surname = gen_names.get_last_name()
            customer = {'first_name':name, 'last_name':surname, 'email':name+"@"+surname+".com"}

            response = self.client.post(url, customer)

            # Create expected customer, now includes the id
            customer.update({
                'id': i+1,
                'details': self.get_test_url(self.CUST_DET_ENDP, args=[i+1])
            })

            created_customers.append(customer)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, customer)

        self.assertEqual(20, Customer.objects.count())

        # Transform customers
        customers_in_db = CustomerSerializerList(Customer.objects.all(), many=True).data

        for customer in customers_in_db:
            customer['details'] = self.URL_TEST_PREFIX + customer['details']

        self.assertEqual(created_customers, customers_in_db)


    def test_get_detail_unkown_customer(self):
        """
        Verify that the customers detail endpoint returns customer info.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get details
        url = self.get_url(self.CUST_DET_ENDP, args=[c.pk+1])
        response = self.client.get(url)

        # Confirm it's an ERROR
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_detail_one_customer(self):
        """
        Verify that the customers detail endpoint returns customer info.
        This is a basic test with only 1 customer.
        This tests the GET endpoint /loyal/customer/${id}
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get details
        url = self.get_url(self.CUST_DET_ENDP, args=[c.pk])
        response = self.client.get(url)

        expected_customer = dict(self.new_customer)
        expected_customer.update({
            'num_stamps': 0,
            'stamps': self.get_test_url(self.STAMP_LIST_ENDP, args=[c.pk]),
            'num_vouchers': 0,
            'vouchers': self.get_test_url(self.VOUCH_LIST_ENDP, args=[c.pk]),
            'num_purchases': 0,
            'purchases': self.get_test_url(self.SALE_LIST_ENDP, args=[c.pk]),
        })

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_customer, response.data)


    def test_get_detail_one_customer_with_counters(self):
        """
        Verify that the customers detail endpoint returns customer info.
        This is a basic test with only 1 customer but wih data on the
        counters.
        This tests the GET endpoint /loyal/customer/${id}
        """

        num_sales = 3
        num_vouchers = 2

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        for _ in xrange(num_sales):
            s = Sale(customer=c, date=timezone.now())
            s.save()

        p = Product(**self.new_product)
        p.save()

        st = Stamp(owned_by=c, obtained_with=p, grouped_in=None)
        st.save()

        for _ in xrange(num_vouchers):
            v = Voucher(owned_by=c, redeemed_with=None)
            v.save()

        # Get details
        url = self.get_url(self.CUST_DET_ENDP, args=[c.pk])
        response = self.client.get(url)

        expected_customer = dict(self.new_customer)
        expected_customer = dict(self.new_customer)
        expected_customer.update({
            'num_stamps': 1,
            'stamps': self.get_test_url(self.STAMP_LIST_ENDP, args=[c.pk]),
            'num_vouchers': 2,
            'vouchers': self.get_test_url(self.VOUCH_LIST_ENDP, args=[c.pk]),
            'num_purchases': 3,
            'purchases': self.get_test_url(self.SALE_LIST_ENDP, args=[c.pk]),
        })

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_customer, response.data)
