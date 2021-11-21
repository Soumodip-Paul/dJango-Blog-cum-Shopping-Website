from django.contrib import admin
from .models import PaymentDetail, Product,Contact,PlacedOrder

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name', 'product_category', 'product_price', 'date')
class ContactAdmin(admin.ModelAdmin):
    list_display = ('msg_id','name', 'email', 'date')
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'order_status', 'price', 'pin_code', 'date')
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','ORDERID', 'TXNID', 'STATUS', 'TXNAMOUNT','TXNDATE')
    def has_change_permission(self, request, obj=None):
        return False
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(PlacedOrder,OrderAdmin)
admin.site.register(PaymentDetail,PaymentAdmin)
