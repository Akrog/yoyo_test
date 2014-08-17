#    from django.db.models import Count

from django.core.management.base import BaseCommand
from loyal.models import Customer, Product, Sale, Stamp, Voucher
import sys

import random
import names as gen_names
from django.utils import timezone

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    num_customers = 100
    num_products = num_customers * 10


    def _create_customers(self):
        print "Adding {0} customers ".format(self.num_customers),
        for _ in xrange(self.num_customers):
            name = gen_names.get_first_name()
            surname = gen_names.get_last_name()
            user = Customer(first_name=name, last_name=surname, email=name+"@"+surname+".com")
            user.save()
            sys.stdout.write('.')

        print "OK"



    def _create_products(self):
        print "Adding {0} products ".format(self.num_products),
        serial_num_int = 1

        # Products are manufactured more than 30 days ago
        min_delta = - timezone.timedelta(days=30).total_seconds()
        max_delta = 2 * min_delta
        now = timezone.now()

        for _ in xrange(self.num_products):
            # Random product type
            product_type = random.randint(0, len(Product.PRODUCT_CHOICES)-1)

            # Get how it must be stored in the DB
            kind = Product.PRODUCT_CHOICES[product_type][0]

            sale = None

            # Generate a 10 digit serial number
            serial_num = "{0:0>10d}".format(serial_num_int)
            serial_num_int += 1

            # Create a random date
            date = now - timezone.timedelta(seconds=random.randint(max_delta,min_delta))

            #Create the product
            product = Product(kind=kind, sale=sale, date=date, serial_num=serial_num)
            product.save()

            sys.stdout.write('.')

        print "OK"



    def _create_sales_and_stamps(self):
        # All sales will be in the last 30 days
        max_delta = - timezone.timedelta(days=30).total_seconds()
        now = timezone.now()

        # We'll only sell 80% of the total number of products
        products_to_sell = int(0.8 * self.num_products)

        # We'll generate a random number of sales
        num_sales = random.randint(self.num_customers, products_to_sell/2)
        products_sold = 0

        print "Creating {0} sales ".format(num_sales),

        for i in xrange(num_sales):
            # Create random sale
            date = now - timezone.timedelta(seconds=random.randint(max_delta,0))
            customer_num = random.randint(1, self.num_customers)
            customer = Customer.objects.get(pk=customer_num)
            sale = Sale(customer=customer, date=date)
            sale.save()

            # Attach products to customer
            randomize_products = products_to_sell - (num_sales - i)
            num_products = random.randint(1, randomize_products)

            for i in xrange(products_sold+1, products_sold+num_products+1):
                product = Product.objects.get(pk=i)
                product.sale = sale
                product.save()

                # If it's a Widget we should add a Stamp
                if product.kind == Product.WIDGET:
                    stamp = Stamp(owned_by=customer, obtained_with=product, grouped_in=None)
                    stamp.save()

            products_to_sell -= num_products
            products_sold += num_products

            sys.stdout.write('.')

        print "OK"

    def _create_vocheurs(self):
        for customer in Customer.objects.values_list('pk',flat=True).all():
            stamps = Stamp.objects.filter(given_with__sold_in__customer=customer)
            for i in xrange(9, stamps.count(), 10):
                to_voucher = stamps[i-9:i+1]
                voucher = Voucher(redeemed_in=None)
                voucher.save()
                for x in to_voucher:
                    x.for_voch = voucher
                    x.save()

        #r = Stamp.objects.value('given_with__sold_in__customer__pk').annotate(count=Count('pk'))
        #Sale.customer
        pass


    def _create_free_stamps(self):
        free_stamps = self.num_customers
        print "Creating {0} free stamps".format(free_stamps),

        for _ in xrange(free_stamps):
            # Pick a random customer
            customer_id = random.randint(1, self.num_customers)
            customer = Customer.objects.get(pk=customer_id)

            # Create a free stamp for that user
            stamp = Stamp(owned_by=customer)
            stamp.save()
            sys.stdout.write('.')

        print "OK"


    def _create_free_vouchers(self):
        free_vouchers = self.num_customers / 2
        print "Creating {0} free vouchers".format(free_vouchers),

        for _ in xrange(free_vouchers):
            # Pick a random customer
            customer_id = random.randint(1, self.num_customers)
            customer = Customer.objects.get(pk=customer_id)

            # Add a free voucher to the customer
            voucher = Voucher(owned_by=customer)
            voucher.save()
            sys.stdout.write('.')

        print "OK"


    def _redeem_vocheurs(self):
        # We'll redeem 50% of the vouchers
        num_vouchers = Voucher.objects.count()
        num_redeem = num_vouchers / 2

        print "Redeeming {0} vouchers from {1}".format(num_redeem, num_vouchers),

        # Get the products that will be acquired with those vouchers
        products = list(Product.objects.filter(voucher__isnull=True)[:num_redeem])
        for voucher in Voucher.objects.all()[:num_redeem]:
            voucher.redeemed_with = products.pop()
            voucher.save()
            sys.stdout.write('.')


        print "OK"


    def handle(self, *args, **options):
        random.seed(2048)

        print "Populating DB"
        self._create_customers()
        self._create_products()
        self._create_sales_and_stamps()
        self._create_free_stamps()
        self._create_free_vouchers()
        self._redeem_vocheurs()
