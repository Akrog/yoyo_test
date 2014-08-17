from rest_framework import generics
from loyal.models import Stamp, Customer
from loyal.serializers import StampSerializer
from django.http import Http404


class StampList(generics.ListCreateAPIView):
    """
    This endpoint gives the stamps for a given customer and allows to add stamps to the customer.
        obtained_with: The product which purchase generated this stamp
        grouped_in: In which voucher has this stamp been grouped
    """

    serializer_class = StampSerializer

    def get_queryset(self):
        owned_by = self.kwargs.get('pk',None)

        try:
            customer = Customer.objects.get(pk=owned_by)
        except Customer.DoesNotExist:
            raise Http404

        return customer.stamp_set.all()
