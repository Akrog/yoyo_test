from django.test import TestCase

from loyal.models import Customer

class TestCustomer(TestCase):
    def test_creation(self):
        first_name = "John"
        last_name  = "Doe"
        email      = "john.doe@gmail.com"

        # Create customer
        c = Customer(first_name=first_name, last_name=last_name, email=email)
        c.save()

        # Retrieve customers from DB
        customers = Customer.objects.all()

        # We must only have created customer
        self.assertEqual(1, len(customers))
        self.assertEqual(c, customers[0])
