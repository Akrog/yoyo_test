from rest_framework import serializers
from loyal.models import Voucher, Customer

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = ('date', 'redeemed_with')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']
        attrs['owned_by'] = Customer.objects.get(pk=pk)
        return Voucher(**attrs)
