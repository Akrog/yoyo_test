from rest_framework import generics
from loyal.models import Voucher, Customer
from loyal.serializers import VoucherSerializer, VoucherListSerializer, VoucherDetailSerializer
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

class VoucherListAllView(generics.ListAPIView):
    """
    This endpoint show all vouchers
    """

    queryset = Voucher.objects.all()
    serializer_class = VoucherListSerializer


class VoucherDetailView(generics.RetrieveUpdateAPIView):
    """
    This endpoint gives vouchers details and allows us to modify an existing voucher
    """

    queryset = Voucher.objects.all()
    serializer_class = VoucherDetailSerializer
