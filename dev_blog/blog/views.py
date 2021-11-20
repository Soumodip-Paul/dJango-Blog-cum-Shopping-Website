from django.http.response import Http404
from django.shortcuts import redirect, render
from .models import BlogPost

# Create your views here.
def index(req):
    categories = BlogPost.objects.values('blog_category')
    cats = [ cat["blog_category"] for cat in categories ] 
    return render(req, 'blog/index.html',{'title':'blog','categories': cats})
def post(req,id): 
    try: 
        post = BlogPost.objects.get(blog_id=id)
        postedItem = {"title": post.blog_title, "date" : post.date, "content": post.blog_content, "image" : post.blog_image, "category": post.blog_category, "author": post.blog_author }
        return render(req,'blog/post.html', postedItem)
    except BlogPost.DoesNotExist:
        raise Http404("Post does not exists")
def postItem(req): 
    return redirect('blog')