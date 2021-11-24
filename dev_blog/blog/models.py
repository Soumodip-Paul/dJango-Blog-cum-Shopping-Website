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
def get_sentinel_category():
    return VideoCategory.objects.get_or_create(category_name='deleted',category_author="admin")[0]
# Create your models here.
class BlogPost(models.Model): 
    blog_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='d')
    blog_id = models.AutoField(primary_key=True)
    blog_title = models.CharField(max_length=50)
    blog_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),editable=False) #models.CharField(max_length=50)
    blog_image = models.ImageField(upload_to="blog/image", default="", null=True,blank=True)
    blog_category = models.CharField(max_length=30)
    date = models.DateTimeField()
    blog_content = models.TextField()
    def __str__(self) -> str:
        return str(self.blog_id) + "( " + self.blog_title + " )"

class VideoCategory(models.Model): 
    category_name = models.CharField(max_length=50,default='',unique=True)
    category_desc = models.TextField()
    category_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='d')
    category_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),editable=False)
    category_id=models.AutoField(primary_key=True)
    category_image = models.ImageField(upload_to="blog/image", default='',)
    date = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return str(self.category_id) + "(" + self.category_name +")"

class YoutubeVideo(models.Model): 
    # video_name = models.CharField(max_length=50,default='')
    youtube_video_id = models.CharField(max_length=20,default='')
    video_category = models.ForeignKey(VideoCategory,on_delete=models.SET(get_sentinel_category),)
    video_status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='d')
    video_author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET(get_sentinel_user),editable=False)
    video_id=models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.youtube_video_id