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

        free_vouch = {"redeemed_with": None, "date": response.data.get("date", None)}
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
        voucher_data ["date"] = response.data.get("date", None)
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
