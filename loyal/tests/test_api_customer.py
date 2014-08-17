from rest_framework import status
from rest_framework.test import APITestCase

from django.core.urlresolvers import reverse

from loyal.models import Customer


class APICustomer(APITestCase):

    new_customer = {'first_name':"John",
                    'last_name':"Doe",
                    'email': "john.doe@gmail.com"}

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

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqual(self.new_customer, response.data[0])



    def test_create_one_customer(self):
        """
        Verify that the customers list endpoint for customer creation works.
        Simple test that will POST only 1 new customer
        """

        url = reverse('loyal:customer-list')
        response = self.client.post(url, self.new_customer)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.new_customer)



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

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.new_customer, response.data)
