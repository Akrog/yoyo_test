from rest_framework import serializers
from loyal.models import Stamp, Customer
from django.http import Http404
from rest_framework.reverse import reverse


class StampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stamp
        fields = ('obtained_with', 'grouped_in')

    def restore_object(self, attrs, instance=None):
        pk = self.context['view'].kwargs['pk']

        try:
            attrs['owned_by'] = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

        return Stamp(**attrs)


class StampListSerializer(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='loyal:stamp:stamp-detail')

    class Meta:
        model = Stamp
        fields = ('id', 'link', 'owned_by', 'obtained_with', 'grouped_in')


class StampDetailSerializer(serializers.ModelSerializer):
    #owner_details = serializers.HyperlinkedIdentityField(view_name='loyal:customer:stamp-detail')
    owner_details = serializers.SerializerMethodField('get_owner_url')

    class Meta:
        model = Stamp
        fields = ('id', 'owned_by', 'owner_details', 'obtained_with', 'grouped_in')

    def get_owner_url(self, obj):
        #customer = obj['given_with__sold_in__customer__pk']
        return reverse('loyal:customer:customer-detail', args=[obj.owned_by.pk], request=self.context['request'])
