from rest_framework import serializers
from loyal.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email')

class CustomerSerializerDetail(serializers.ModelSerializer):
    num_stamps = serializers.IntegerField(source='stamp_set.count', read_only=True)
    num_vouchers = serializers.IntegerField(source='voucher_set.count', read_only=True)
    num_purchases = serializers.IntegerField(source='sale_set.count', read_only=True)
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'num_stamps', 'num_vouchers', 'num_purchases')
