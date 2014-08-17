from rest_framework import status
from rest_framework.test import APITestCase

from django.core.urlresolvers import reverse
from django.utils import timezone

from loyal.models import Customer, Product, Sale, Stamp, Voucher


class APICustomer(APITestCase):
    CUST_LIST_ENDP  = 0
    CUST_DET_ENDP   = 1
    STAMP_LIST_ENDP = 2
    VOUCH_LIST_ENDP = 3

    namespace_path = ['loyal', 'customer']


    endpoints = {
        CUST_LIST_ENDP  :'customer-list',
        CUST_DET_ENDP   :'customer-detail',
        STAMP_LIST_ENDP :'stamp-list',
        VOUCH_LIST_ENDP :'voucher-list',
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


    def get_url(self, entrypoint, *args, **kwargs):
        namespace = ":".join(self.namespace_path)
        return reverse(namespace + ":" + self.endpoints[entrypoint], *args, **kwargs)


    def test_get_list_empty(self):
        """
        Test that endpoint's GET for customers list is working.
        On an empty DB it should always return empty list.
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
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.CUST_LIST_ENDP)
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
        url = self.get_url(self.CUST_LIST_ENDP)
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
        url = self.get_url(self.CUST_DET_ENDP, args=[c.pk])
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
        url = self.get_url(self.CUST_DET_ENDP, args=[c.pk])
        response = self.client.get(url)

        expected_customer = dict(self.new_customer)
        expected_customer.update ({'num_stamps':1, 'num_vouchers':2, 'num_purchases':3})

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_customer, response.data)


    def test_stamp_list_empty(self):
        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_create_free_stamp(self):
        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create stamp
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.post(url)

        # Confirm it's OK
        free_stamp = {"obtained_with": None, "grouped_in": None}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, free_stamp)


    def test_create_stamp(self):
        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create product in DB
        p = Product(**self.new_product)
        p.save()

        # Create stamp
        stamp_data = {"obtained_with": p.pk, "grouped_in": None}
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, stamp_data)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, stamp_data)


    def test_voucher_list_empty(self):
        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_create_free_voucher(self):
        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create voucher
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.post(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        free_vouch = {"redeemed_with": None, "date": response.data.get("date", None)}
        self.assertEqual(response.data, free_vouch)


    def test_create_voucher(self):
        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create product in DB
        p = Product(**self.new_product)
        p.save()

        # Create voucher
        voucher_data = {"redeemed_with": p.pk}
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, voucher_data)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        voucher_data ["date"] = response.data.get("date", None)
        self.assertEqual(response.data, voucher_data)
