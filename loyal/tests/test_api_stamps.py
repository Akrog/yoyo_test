from rest_framework import status
from loyal.models import Customer, Product, Stamp
from .yoyo_api_testcase import YoyoAPITestCase

import names as gen_names



class APIStamp(YoyoAPITestCase):
    """
    This class tests following endpoints
        /loyal/customer/stamps
    """


    def test_stamp_list_empty(self):
        """
        Test that for a given customer initially the stamp list is empty.
        This tests the GET from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_stamp_list_populated(self):
        """
        Test that for a given customer we can see it's stamps.
        We create 2 stamps directly in the DB, one free and one from purchasing a product.
        This tests the GET from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Create product
        p = Product(**self.new_product)
        p.save()

        # Create stamp
        s = Stamp(owned_by=c, obtained_with=p, grouped_in=None)
        s.save()

        # Create free stamp
        s = Stamp(owned_by=c)
        s.save()

        # Get list
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

        stamp_data = {
            'obtained_with': p.pk,
            'grouped_in': None,
            'link': self.get_non_customer_url(self.STAMP_ENDP, args=[1]),
        }
        self.assertEqual(response.data[0], stamp_data)

        stamp_data.update({
            'obtained_with': None,
            'link': self.get_non_customer_url(self.STAMP_ENDP, args=[2]),
        })
        self.assertEqual(response.data[1], stamp_data)


    def test_create_free_stamp(self):
        """
        Test that creates a free stamp for a given customer.
        This tests the POST from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create stamp
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.post(url)

        # Confirm it's OK
        free_stamp = {
            "obtained_with": None,
            "grouped_in": None,
            'link': self.get_non_customer_url(self.STAMP_ENDP, args=[1]),
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, free_stamp)


    def test_create_stamp(self):
        """
        Test that creates a normal stamp for a given customer.
        This tests the POST from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create product in DB
        p = Product(**self.new_product)
        p.save()

        # Create stamp
        stamp_data = {
            "obtained_with": p.pk,
            "grouped_in": None,
        }
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, stamp_data)

        stamp_data['link'] = self.get_non_customer_url(self.STAMP_ENDP, args=[1])

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, stamp_data)

    def test_create_stamp_impossible_product(self):
        """
        Test that tries to create a normal stamp for a given customer with a non existant product.
        This tests the POST from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create stamp
        stamp_data = {"obtained_with": 10, "grouped_in": None}
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, stamp_data)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_stamp_non_existan_owner(self):
        """
        Test that tries to create a normal stamp with an unkown owner
        This tests the POST from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create product in DB
        p = Product(**self.new_product)
        p.save()

        # Create stamp through API
        stamp_data = {"obtained_with": p.pk, "grouped_in": None}
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk+1])
        response = self.client.post(url, stamp_data)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_stamp_product_occupied(self):
        """
        Test that tries to create a normal stamp with an unkown owner
        This tests the POST from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create product in DB
        p = Product(**self.new_product)
        p.save()

        # Stamp product in DB
        st = Stamp(owned_by=c, obtained_with=p, grouped_in=None)
        st.save()

        # Create stamp through API
        stamp_data = {"obtained_with": p.pk, "grouped_in": None}
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, stamp_data)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
