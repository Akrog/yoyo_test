from django.db import models

# Create your models here.

class Customer(models.Model):
    """
    Customer model
        first_name
        last_name
        email
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()

    def __unicode__(self):
        return " ".join([self.first_name, self.last_name, "<" + self.email + ">"])
