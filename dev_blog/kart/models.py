from django.db import models

ORDER_TYPES = [
    ('u', 'Payment Not Done'),
    ('f', 'Payment Failed'),
    ('s', 'Success'),
    ('w', 'Payment withdrawn')
]

# Create your models here.
class Product(models.Model): 
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=300)
    product_image = models.ImageField(upload_to="shop/image", default="")
    product_price = models.IntegerField(default=0)
    product_category = models.CharField(default="", max_length=30)
    product_subcategory = models.CharField(default="",max_length=50)
    date = models.DateField()
    def __str__(self) -> str:
        return str(self.id) + " " + self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    email= models.EmailField(max_length=70)
    desc = models.CharField(max_length=500)
    date = models.DateField()
    def __str__(self) -> str:
        return str(self.msg_id)

class PlacedOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_id=models.IntegerField(default=0)
    order_status=models.CharField(default='u',choices=ORDER_TYPES, max_length=1)
    items_ordered = models.CharField(max_length=100000)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=100)
    date = models.DateField()
    price= models.IntegerField(default=0)
    def __str__(self) -> str:
        return str(self.id)