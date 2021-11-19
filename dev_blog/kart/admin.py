from django.contrib import admin
from .models import Product,Contact,PlacedOrder

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','product_name', 'product_category', 'product_price', 'date')
class ContactAdmin(admin.ModelAdmin):
    list_display = ('msg_id','name', 'email', 'date')
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'pin_code', 'date')
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(PlacedOrder,OrderAdmin)
