from django.db import models

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
    def __str__(self):
        return self.product_name
