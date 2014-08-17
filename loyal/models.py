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



class Voucher(models.Model):
    """
    Voucher model:
        owned_by      -> The customer who owns this voucher
        redeemed_with -> Product acquired by redeeming this voucher
        date          -> When it was created
    """

    owned_by = models.ForeignKey(Customer)
    date = models.DateTimeField(auto_now_add=True, verbose_name='creation date')
    redeemed_with = models.OneToOneField(Product, blank=True, null=True, verbose_name='product acquired redeeming this voucher')

    def __unicode__(self):
        status = "Redeemed" if self.redeemed_with else "Available"
        return " ".join(["[",str(self.pk),"]", self.owned_by.email, "-", status])



class Stamp(models.Model):
    """
    Stamp model:
        owned_by      -> The customer who owns this stamp
        obtained_with -> Which product produced this stamp
        grouped_in    -> In which voucher has been grouped this stamp

    We allow the creation of stamps with no product attached to, in case it's a gift or similar case.
    """

    STAMPS_PER_VOUCHER = 10

    owned_by = models.ForeignKey(Customer)
    obtained_with = models.OneToOneField(Product, blank=True, null=True, verbose_name='product which purchase generated this stamp')
    grouped_in = models.ForeignKey(Voucher, blank=True, null=True, verbose_name='grouped in voucher')

    def __unicode__(self):
        return " ".join(["[", str(self.pk), "]", self.owned_by.email])


    def save(self, *args, **kwargs):
        """
        For every 10 stamps created we have to convert them into 1 voucher.
        So for every stamp we create we check if we have 10 and create the voucher and assign it to the customer.
        """

        is_new_stamp = not self.pk

        # Call the "real" save() method.
        super(Stamp, self).save(*args, **kwargs)

        # Convert to vouchers every 10 stamps
        if is_new_stamp:
            # Get all stamps that have not already been converted to vouchers
            stamps = Stamp.objects.filter(grouped_in__isnull=True, owned_by=self.owned_by)

            for i in xrange(self.STAMPS_PER_VOUCHER-1, stamps.count(), self.STAMPS_PER_VOUCHER):
                # Create new voucher
                voucher = Voucher(owned_by=self.owned_by, redeemed_with=None)
                voucher.save()

                # Get the 10 vouchers
                to_voucher = stamps[i+1-self.STAMPS_PER_VOUCHER:i+1]

                # Now they have been grouped in the new voucher
                for stamp in to_voucher:
                    stamp.grouped_in = voucher
                    stamp.save()
