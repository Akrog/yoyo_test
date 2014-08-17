from rest_framework import status
from rest_framework.test import APITestCase

from django.core.urlresolvers import reverse

from loyal.models import Customer


class APICustomer(APITestCase):

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

        new_customer = {'first_name':"John",
                        'last_name':"Doe",
                        'email': "john.doe@gmail.com"}

        # Create customer
        c = Customer(**new_customer)
        c.save()

        # Get list
        url = reverse('loyal:customer-list')
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqual(new_customer, response.data[0])



    def test_create_one_customer(self):
        """
        Verify that the customers list endpoint for customer creation works.
        Simple test that will POST only 1 new customer
        """

        new_customer = {'first_name':"John",
                        'last_name':"Doe",
                        'email': "john.doe@gmail.com"}

        url = reverse('loyal:customer-list')
        response = self.client.post(url, new_customer)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, new_customer)
