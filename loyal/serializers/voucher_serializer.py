from rest_framework import serializers
from loyal.models import Voucher, Customer
from django.http import Http404

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ('date', 'redeemed_with')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']

        try:
            attrs['owned_by'] = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        return Voucher(**attrs)
