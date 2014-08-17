from django.contrib import admin

from loyal.models import Customer, Sale, Product, Stamp, Voucher

# Register your models here.
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(Product)
admin.site.register(Stamp)
admin.site.register(Voucher)
