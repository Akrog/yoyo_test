from rest_framework import generics
from loyal.models import Sale, Customer
from loyal.serializers import SaleSerializer
from django.http import Http404


class SaleListView(generics.ListCreateAPIView):
    """
    This endpoint gives the sales for a given customer and allows to add sales to the customer.
    """

    serializer_class = SaleSerializer

    def get_queryset(self):
        owned_by = self.kwargs.get('pk',None)

        try:
            customer = Customer.objects.get(pk=owned_by)
        except Customer.DoesNotExist:
            raise Http404

        return customer.sale_set.all()
