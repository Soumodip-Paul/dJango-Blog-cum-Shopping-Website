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
    list_display = ['blog_id', 'blog_author', 'blog_title' , 'blog_status', 'blog_category' ,'date']
    ordering = ['date']
    actions = [make_published, make_draft, withdrawArticle]
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

# admin.site.register(BlogPost, BlogAdmin)
    
