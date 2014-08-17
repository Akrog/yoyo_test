from rest_framework import generics
from loyal.models import Voucher, Customer
from loyal.serializers import VoucherSerializer
from django.http import Http404


class VoucherListView(generics.ListCreateAPIView):
    """
    This endpoint gives the vouchers for a given customer and allows adding new vouchers to the customer.
        date: When the voucher was created
        redeemed_with: with which product was this voucher redeemed
    """

    serializer_class = VoucherSerializer

    def get_queryset(self):
        owned_by = self.kwargs.get('pk',None)

        try:
            customer = Customer.objects.get(pk=owned_by)
        except Customer.DoesNotExist:
            raise Http404

        return customer.voucher_set.all()
