from rest_framework import status
from rest_framework.test import APITestCase

from django.core.urlresolvers import reverse
from django.utils import timezone

from loyal.models import Customer, Product, Sale, Stamp, Voucher


class APICustomer(APITestCase):

    new_customer = {'first_name':"John",
                    'last_name':"Doe",
                    'email': "john.doe@gmail.com"}

    new_product = {
        'kind': Product.WIDGET,
        'date': timezone.now(),
        'serial_num': "1",
        'sale': None
    }

    def test_get_list_empty(self):
        """
        Test that endpoint's GET for customers list is working.
        On an empty DB it should always return empty list.
        """

        # Get list
        url = reverse('loyal:customer-list')
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])



    def test_get_list_one_customer(self):
        """
        Verify that the customers list endpoint returns customers from the DB.
        This is a basic test with only 1 customer.
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = reverse('loyal:customer-list')
        response = self.client.get(url)

        # Create expected customer, now includes the id
        expected_customer = dict(self.new_customer)
        expected_customer['id'] = c.pk

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqual(expected_customer, response.data[0])



    def test_list_create_one_customer(self):
        """
        Verify that the customers list endpoint for customer creation works.
        Simple test that will POST only 1 new customer
        """

        # POST creation
        url = reverse('loyal:customer-list')
        response = self.client.post(url, self.new_customer)

        # Create expected customer, now includes the id
        expected_customer = dict(self.new_customer)
        expected_customer['id'] = 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_customer)



    def test_get_detail_one_customer(self):
        """
        Verify that the customers detail endpoint returns customer info.
        This is a basic test with only 1 customer.
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get details
        url = reverse('loyal:customer-detail', args=[c.pk])
        response = self.client.get(url)

        expected_customer = dict(self.new_customer)
        expected_customer['num_stamps'] = 0
        expected_customer['num_vouchers'] = 0
        expected_customer['num_purchases'] = 0

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_customer, response.data)


    def test_get_detail_one_customer_with_counters(self):
        """
        Verify that the customers detail endpoint returns customer info.
        This is a basic test with only 1 customer but wih data on the
        counters.
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
        url = reverse('loyal:customer-detail', args=[c.pk])
        response = self.client.get(url)

        expected_customer = dict(self.new_customer)
        expected_customer['num_stamps'] = 1
        expected_customer['num_vouchers'] = 2
        expected_customer['num_purchases'] = 3

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_customer, response.data)
