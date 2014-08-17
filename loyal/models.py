from django.db import models
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
    """
    Customer model:
        first_name
        last_name
        email
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()

    def __unicode__(self):
        return " ".join([self.first_name, self.last_name, "<" + self.email + ">"])



class Sale(models.Model):
    """
    Purchase model:
        customer -> Who made the purchase
        date     -> When was this purchase made
    """

    customer = models.ForeignKey(Customer)
    date = models.DateTimeField(default=timezone.now, verbose_name='purchase date')

    def __unicode__(self):
        return " ".join([str(self.pk), "-", self.customer.email])



class Product(models.Model):
    """
    Product model:
        kind       -> What kind or product we have
        date       -> When was it manufactured
        serial_num -> What is the serial number for the product
        sale       -> If not null is in what purchase it was sold
    """

    WIDGET=0
    GIZMO=1
    PRODUCT_CHOICES = (
        (WIDGET, 'widget'),
        (GIZMO, 'gizmo')
    )

    kind = models.SmallIntegerField(choices=PRODUCT_CHOICES, verbose_name='kind of product')
    date = models.DateTimeField(default=timezone.now, verbose_name='manufacture date')
    serial_num = models.CharField(unique=True, max_length=20, verbose_name='serial number')
    sale = models.ForeignKey(Sale, blank=True, null=True)

    def __unicode__(self):
        return " ".join([self.PRODUCT_CHOICES[self.kind][1], "[", str(self.pk), "]"])
