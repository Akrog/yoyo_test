from rest_framework import status
from loyal.models import Customer, Product, Sale, Stamp, Voucher
from .yoyo_api_testcase import YoyoAPITestCase

import names as gen_names



class APIVoucher(YoyoAPITestCase):
    """
    This class tests following endpoints
        /loyal/customer/vouchers
    """


    def test_voucher_list_empty(self):
        """
        Test that for a given customer initially the voucher list is empty.
        This tests the GET endpoint /loyal/customer/${id}/vouchers
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Get list
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


    def test_voucher_list_populated(self):
        """
        Test that for a given customer we can see it's vouchers.
        We create 2 vouchers directly in the DB, one available and one redeemed.
        This tests the GET from endpoint /loyal/customer/${id}/vouchers
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Create product
        p = Product(**self.new_product)
        p.save()

        # Create voucher
        v = Voucher(owned_by=c, redeemed_with=p)
        v.save()

        # Create free voucher
        v = Voucher(owned_by=c)
        v.save()

        # Get list
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.get(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, len(response.data))

        voucher_data = {"redeemed_with": p.pk,
                        "date": response.data[0].get("date", None),
                        'link': self.get_non_customer_url(self.VOUCHER_ENDP, args=[1])}
        self.assertEqual(response.data[0], voucher_data)

        voucher_data = {"redeemed_with": None,
                        "date": response.data[1].get("date", None),
                        'link': self.get_non_customer_url(self.VOUCHER_ENDP, args=[2])}
        self.assertEqual(response.data[1], voucher_data)


    def test_create_free_voucher(self):
        """
        Test that creates a free voucher for a given customer.
        This tests the POST from endpoint /loyal/customer/${id}/vouchers
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create voucher
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.post(url)

        # Confirm it's OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        free_vouch = {
            "redeemed_with": None,
            "date": response.data.get("date", None),
            'link': self.get_non_customer_url(self.VOUCHER_ENDP, args=[1]),
        }
        self.assertEqual(response.data, free_vouch)


    def test_create_voucher(self):
        """
        Test that creates a redeemed voucher for a given customer.
        This tests the POST from endpoint /loyal/customer/${id}/vouchers
        """

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
        voucher_data.update({
            'date':response.data.get("date", None),
            'link': self.get_non_customer_url(self.VOUCHER_ENDP, args=[1]),
        })

        self.assertEqual(response.data, voucher_data)


    def test_voucher_autogeneration(self):
        """
        Test that for every 10 stamps that we create for a customer a voucher is generated.
        This tests the POST from endpoint /loyal/customer/${id}/stamps.
        """

        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Create 10 stamps
        url = self.get_url(self.STAMP_LIST_ENDP, args=[c.pk])
        for _ in xrange(10):
            response = self.client.post(url)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Retrieve stamps from DB
        stamps = Stamp.objects.all()
        self.assertEqual(10, len(stamps))

        # Retrieve vouchers from DB
        vouchers = Voucher.objects.all()
        self.assertEqual(1, len(vouchers))

        # Confirm that there are 10 stamps linked to the voucher
        self.assertEqual(10, vouchers[0].stamp_set.count())


    def test_create_voucher_non_existan_owner(self):
        """
        Test that tries to create a normal voucher with an unkown owner
        This tests the POST from endpoint /loyal/customer/${id}/vouchers.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create stamp through API
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk+1])
        response = self.client.post(url, {})

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_voucher_non_existan_redeem_product(self):
        """
        Test that tries to create a normal voucher to redeem a non existant product
        This tests the POST from endpoint /loyal/customer/${id}/vouchers.
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create stamp through API
        voucher_data = {"redeemed_with": 10}
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk+1])
        response = self.client.post(url, voucher_data)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_voucher_product_occupied(self):
        """
        Test that tries to create a redeemed voucher for a product that has already been redeemed.
        This tests the POST from endpoint /loyal/customer/${id}/vouchers
        """

        # Create customer in DB
        c = Customer(**self.new_customer)
        c.save()

        # Create product in DB
        p = Product(**self.new_product)
        p.save()

        # Create voucher in DB
        v = Voucher(owned_by=c, redeemed_with=p)
        v.save()

        # Create voucher through API
        voucher_data = {"redeemed_with": p.pk}
        url = self.get_url(self.VOUCH_LIST_ENDP, args=[c.pk])
        response = self.client.post(url, voucher_data)

        # Confirm it's not OK
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
