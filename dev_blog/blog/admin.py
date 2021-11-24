from django.contrib import admin
from django.db import models
from .models import BlogPost,VideoCategory, YoutubeVideo

admin.site.site_header = "Cool Developer Admin Panel"
admin.site.site_title = " Cool Developer Admin Portal"
admin.site.index_title = "Welcome to Cool Developer Admin Portal"

@admin.action(description='Mark selected content as published')
def make_published(modeladmin, request, queryset):
    queryset.update(blog_status='p')  

@admin.action(description='Draft COntent')
def make_draft(modeladmin, request, queryset):
    queryset.update(blog_status='d')

@admin.action(description='Withdraw Content')
def withdrawContent(modeladmin, request, queryset):
    queryset.update(blog_status='w')

# Register your models here
@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin): 
    list_display = ['blog_id', 'blog_author', 'blog_title' , 'blog_status', 'blog_category' ,'date']
    ordering = ['date']
    actions = [make_published, make_draft, withdrawContent]
    list_display_links = ('blog_id', 'blog_title',)
    list_editable = ('blog_status', 'blog_category')
    search_fields = ('blog_title', 'blog_author', 'date', 'blog_status', 'blog_category')
    list_per_page = 50

    def get_queryset(self, request):
        qs = super(BlogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(blog_author=request.user)
    def save_model(self, request, obj, form, change):
        # associating the current logged in user to the client_id
        obj.blog_author = request.user
        super().save_model(request, obj, form, change)
    class Media: 
        js = ["js/tinymce.js"]

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_id', 'category_name', 'category_status' , 'category_author', 'date']
    ordering = ['date']
    actions = [make_published, make_draft, withdrawContent]
    list_display_links = ('category_id', "date", 'category_name')
    list_editable = ('category_status', )
    search_fields = ('category_id', 'category_name', 'date', 'category_desc', )
    list_per_page = 50
    def get_queryset(self, request):
        qs = super(VideoCategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(category_author=request.user)
    def save_model(self, request, obj, form, change):
        # associating the current logged in user to the client_id
        obj.category_author = request.user
        super().save_model(request, obj, form, change)

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display = ['video_id', 'youtube_video_id', 'video_status' , 'video_author', 'date']
    ordering = ['date']
    actions = [make_published, make_draft, withdrawContent]
    list_display_links = ('video_id', "date", 'youtube_video_id')
    list_editable = ('video_status', )
    search_fields = ('video_id', 'youtube_video_name', 'date',)
    list_per_page = 50
    def get_queryset(self, request):
        qs = super(YoutubeVideoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(video_author=request.user)
    def save_model(self, request, obj, form, change):
        # associating the current logged in user to the client_id
        obj.video_author = request.user
        super().save_model(request, obj, form, change)
# admin.site.register(BlogPost, BlogAdmin)
    
