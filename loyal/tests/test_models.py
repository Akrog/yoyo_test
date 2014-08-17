from django.test import TestCase
from django.utils import timezone

from loyal.models import Customer, Sale, Product


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


    def test_customer_creation(self):
        # Create customer
        c = Customer(**self.new_customer)
        c.save()

        # Retrieve customers from DB
        customers = Customer.objects.all()

        # We must only have created customer
        self.assertEqual(1, len(customers))
        self.assertEqual(c, customers[0])


    def test_product_creation(self):
        # Create product
        p = Product(**self.new_product)
        p.save()

        # Retrieve product from DB
        product = Product.objects.all()

        # We must only have created product
        self.assertEqual(1, len(product))
        self.assertEqual(p, product[0])


    def test_sale_creation(self):
        # Create a new customer
        c = Customer(**self.new_customer)
        c.save()

        s = Sale(customer=c, date=timezone.now())
        s.save()

        customers = Customer.objects.all()

        # Retrieve Sale from DB
        sales = Sale.objects.all()

        # We must only have created sale
        self.assertEqual(1, len(sales))
        self.assertEqual(s, sales[0])


    def test_sale_creation_assign_product(self):
        c = Customer(**self.new_customer)
        c.save()

        s = Sale(customer=c, date=timezone.now())
        s.save()

        p = Product(**self.new_product)
        p.sale = s;
        p.save()

        # We must only have created sale
        sales = Sale.objects.all()
        self.assertEqual(1, len(sales))
        self.assertEqual(s, sales[0])

        # And it must be linked to the product
        products_sold = sales[0].product_set.all()
        self.assertEqual(1, len(products_sold))
        self.assertEqual(p, products_sold[0])
