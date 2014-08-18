from rest_framework import serializers
from loyal.models import Customer

from rest_framework.reverse import reverse

class CustomerSerializerList(serializers.ModelSerializer):
    details = serializers.HyperlinkedIdentityField(view_name='loyal:customer:customer-detail')

    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email', 'details')


class CustomerSerializerDetail(serializers.ModelSerializer):
    available_stamps = serializers.SerializerMethodField('get_available_stamps')
    total_stamps = serializers.IntegerField(source='stamp_set.count', read_only=True)
    stamps = serializers.HyperlinkedIdentityField(view_name='loyal:customer:stamp-list')

    available_vouchers = serializers.SerializerMethodField('get_available_vouchers')
    total_vouchers = serializers.IntegerField(source='voucher_set.count', read_only=True)
    vouchers = serializers.HyperlinkedIdentityField(view_name='loyal:customer:voucher-list')

    num_purchases = serializers.IntegerField(source='sale_set.count', read_only=True)
    purchases = serializers.HyperlinkedIdentityField(view_name='loyal:customer:sale-list')

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email',
                  'available_stamps',  'total_stamps', 'stamps',
                  'available_vouchers', 'total_vouchers',  'vouchers',
                  'num_purchases', 'purchases')

    def get_available_stamps(self, obj):
        return obj.stamp_set.filter(grouped_in__isnull=True).count()

    def get_available_vouchers(self, obj):
        return obj.voucher_set.filter(redeemed_with__isnull=True).count()
