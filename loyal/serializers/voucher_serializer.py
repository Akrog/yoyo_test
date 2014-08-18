from rest_framework import serializers
from loyal.models import Voucher, Customer
from django.http import Http404
from rest_framework.reverse import reverse

class VoucherSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='loyal:voucher:voucher-detail')

    class Meta:
        model = Voucher
        fields = ('date', 'redeemed_with', 'link')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']

        try:
            attrs['owned_by'] = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        return Voucher(**attrs)


class VoucherListSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='loyal:voucher:voucher-detail')

    class Meta:
        model = Voucher
        fields = ('id', 'link', 'owned_by', 'redeemed_with', 'date')


class VoucherDetailSerializer(serializers.ModelSerializer):
    owner_details = serializers.SerializerMethodField('get_owner_url')
    stamps = serializers.HyperlinkedRelatedField(source='stamp_set', many=True, read_only=True,
                                                 view_name='loyal:stamp:stamp-detail')
    class Meta:
        model = Voucher
        fields = ('id', 'owned_by', 'owner_details', 'redeemed_with', 'date', 'stamps')

    def get_owner_url(self, obj):
        return reverse('loyal:customer:customer-detail', args=[obj.owned_by.pk], request=self.context['request'])
