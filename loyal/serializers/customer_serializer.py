from rest_framework import serializers
from loyal.models import Customer

from rest_framework.reverse import reverse

class CustomerSerializerList(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='loyal:customer:customer-detail')

    class Meta:
        model = Customer
        fields = ('id', 'link')


class CustomerSerializerDetail(serializers.ModelSerializer):
    num_stamps = serializers.IntegerField(source='stamp_set.count', read_only=True)
    stamps = serializers.HyperlinkedIdentityField(view_name='loyal:customer:stamp-list')

    num_vouchers = serializers.IntegerField(source='voucher_set.count', read_only=True)
    vouchers = serializers.HyperlinkedIdentityField(view_name='loyal:customer:voucher-list')

    num_purchases = serializers.IntegerField(source='sale_set.count', read_only=True)
    purchases = serializers.HyperlinkedIdentityField(view_name='loyal:customer:sale-list')

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'num_stamps', 'stamps',
                  'num_vouchers', 'vouchers', 'num_purchases', 'purchases')
