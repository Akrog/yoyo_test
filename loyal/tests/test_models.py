from django.test import TestCase
from django.utils import timezone

from loyal.models import Customer, Sale, Product, Stamp, Voucher


class TestModel(TestCase):
    new_product = {
        'kind': Product.WIDGET,
        'date': timezone.now(),
        'serial_num': "1",
        'sale': None
    }

    new_customer = {
        'first_name':"John",
        'last_name':"Doe",
        'email':"john.doe@gmail.com"
    }



    def _creation(self, customer=False, product=False, sale=False):
        c = None; p = None; s = None

        # Create customer
        if customer:
            c = Customer(**self.new_customer)
            c.save()

        # Create sale
        if sale:
            s = Sale(customer=c, date=timezone.now())
            s.save()

        # Create product
        if product:
            p = Product(**self.new_product)
            p.sale = s
            p.save()

        return (c, p, s)



    def test_customer_creation(self):
        # Create customer
        c, _, _ = self._creation(customer=True)

        # Retrieve customers from DB
        customers = Customer.objects.all()

        # We must only have created customer
        self.assertEqual(1, len(customers))
        self.assertEqual(c, customers[0])



    def test_product_creation(self):
        # Create product
        _, p, _ = self._creation(product=True)

        # Retrieve product from DB
        product = Product.objects.all()

        # We must only have created product
        self.assertEqual(1, len(product))
        self.assertEqual(p, product[0])



    def test_sale_creation(self):
        # Create a new customer an empty sale
        c, _, s = self._creation(customer=True, sale=True)

        customers = Customer.objects.all()

        # Retrieve Sale from DB
        sales = Sale.objects.all()

        # We must only have created sale
        self.assertEqual(1, len(sales))
        self.assertEqual(s, sales[0])



    def test_sale_creation_assign_product(self):
        # Create a customer, product and sale
        c, p, s = self._creation(customer=True, product=True, sale=True)

        # Retrieve Sale from DB
        sales = Sale.objects.all()

        # We must only have created sale
        self.assertEqual(1, len(sales))
        self.assertEqual(s, sales[0])

        # And it must be linked to the product
        products_sold = sales[0].product_set.all()
        self.assertEqual(1, len(products_sold))
        self.assertEqual(p, products_sold[0])



    def test_stamp_creation(self):
        # Create a customer and product
        c, p, _ = self._creation(customer=True, product=True)

        # Create a new stamp
        stamp = Stamp(owned_by=c, obtained_with=p, grouped_in=None)
        stamp.save()

        # Retrieve stamps from DB
        stamps = Stamp.objects.all()

        # We must only have created stamp
        self.assertEqual(1, len(stamps))
        self.assertEqual(stamp, stamps[0])



    def test_voucher_creation(self):
        # Create a customer
        c, _, _ = self._creation(customer=True)

        # Create a voucher with no stamps
        voucher = Voucher(owned_by=c, redeemed_with=None)
        voucher.save()

        # Retrieve voucher from DB
        vouchers = Voucher.objects.all()

        # We must only have created stamp
        self.assertEqual(1, len(vouchers))
        self.assertEqual(voucher, vouchers[0])



    def test_voucher_autocreation(self):
        """
        Test that the model logic in Stamp is working correctly.
        This tests adds 10 stamps.
        For every 10 stamps 1 voucher should be automatically added and the
        stamps should be linked to that new voucher.
        """

        # Create a customer and product
        c, _, _ = self._creation(customer=True)

        # Create 9 stamps and confirm that no voucher has been added
        for _ in xrange(Stamp.STAMPS_PER_VOUCHER - 1):
            stamp = Stamp(owned_by=c)
            stamp.save()

        # Retrieve stamps from DB
        stamps = Stamp.objects.all()
        self.assertEqual(9, len(stamps))

        # Retrieve vouchers from DB
        vouchers = Voucher.objects.all()
        self.assertEqual(0, len(vouchers))

        # Add the 10th stamp
        stamp = Stamp(owned_by=c)
        stamp.save()

        # Retrieve stamps from DB
        stamps = Stamp.objects.all()
        self.assertEqual(10, len(stamps))

        # Retrieve vouchers from DB
        vouchers = Voucher.objects.all()
        self.assertEqual(1, len(vouchers))

        # Confirm that the 10 stamps are really linked to the voucher
        self.assertEqual(10, vouchers[0].stamp_set.count())



    def test_voucher_autocreation_19(self):
        """
        Test that the model logic in Stamp is working correctly.
        This test adds 19 stamps.
        For every 10 stamps 1 voucher should be automatically added and the
        stamps should be linked to that new voucher.
        """

        # Create a customer and product
        c, _, _ = self._creation(customer=True)

        # Create 19 stamps
        for _ in xrange((2 * Stamp.STAMPS_PER_VOUCHER) - 1):
            stamp = Stamp(owned_by=c)
            stamp.save()

        # Retrieve stamps from DB
        stamps = Stamp.objects.all()
        self.assertEqual(19, len(stamps))

        # Retrieve vouchers from DB
        vouchers = Voucher.objects.all()
        self.assertEqual(1, len(vouchers))

        # Confirm that there are 10 stamps linked to the voucher
        self.assertEqual(10, vouchers[0].stamp_set.count())

        # Confirm that there are 9 free stamps
        self.assertEqual(9, Stamp.objects.filter(grouped_in__isnull=True).count())
