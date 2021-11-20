from django.db import models

STATUS_CHOICES = [
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]

# Create your models here.
class BlogPost(models.Model): 
    blog_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=50)
    blog_author = models.CharField(max_length=50)
    blog_image = models.ImageField(upload_to="shop/image", default="", null=True,blank=True)
    blog_category = models.CharField(max_length=30)
    date = models.DateTimeField()
    blog_content = models.TextField()
    def __str__(self) -> str:
        return str(self.blog_id) + "( " + self.blog_title + " )"