from django.shortcuts import render
from loyal.models import Customer
from loyal.serializers import CustomerSerializer, CustomerSerializerDetail
from rest_framework import generics

# Create your views here.
class CustomerList(generics.ListCreateAPIView):
    """
    This endpoint lists the customers in the system and allow creation of new
    customers.

    Fields are self-explanatory.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetail(generics.RetrieveAPIView):
    """
    This endpoint shows detailed information of one customer.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializerDetail
