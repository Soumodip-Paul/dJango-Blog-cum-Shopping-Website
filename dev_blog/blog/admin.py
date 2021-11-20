from django.contrib import admin
from .models import BlogPost


@admin.action(description='Mark selected stories as published')
def make_published(modeladmin, request, queryset):
    queryset.update(blog_status='p')  

@admin.action(description='Draft Article')
def make_draft(modeladmin, request, queryset):
    queryset.update(blog_status='d')

@admin.action(description='Withdraw Article')
def withdrawArticle(modeladmin, request, queryset):
    queryset.update(blog_status='w')

# Register your models here
@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin): 
    list_display = ['blog_id', 'blog_author', 'blog_title' , 'blog_status' ,'date']
    ordering = ['date']
    actions = [make_published, make_draft]
    class Media: 
        js = ["js/tinymce.js"]

# admin.site.register(BlogPost, BlogAdmin)
    
