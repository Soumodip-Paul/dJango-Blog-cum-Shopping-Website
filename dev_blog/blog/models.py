from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]
# Create your models here.
class BlogPost(models.Model): 
    blog_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=50)
    blog_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),editable=False) #models.CharField(max_length=50)
    blog_image = models.ImageField(upload_to="shop/image", default="", null=True,blank=True)
    blog_category = models.CharField(max_length=30)
    date = models.DateTimeField()
    blog_content = models.TextField()
    def __str__(self) -> str:
        return str(self.blog_id) + "( " + self.blog_title + " )"