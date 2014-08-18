from django.shortcuts import render
from loyal.models import Customer
from loyal.serializers import CustomerSerializerList, CustomerSerializerDetail
from rest_framework import generics

# Create your views here.
class CustomerListView(generics.ListCreateAPIView):
    """
    This endpoint lists the customers in the system and allows creation of new customers.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializerList

class CustomerDetailView(generics.RetrieveAPIView):
    """
    This endpoint shows detailed information of one customer.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializerDetail
