from django.http.response import Http404
from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import BlogPost
from . import utils

# Create your views here.
def index(req):
    categories = BlogPost.objects.values('blog_category')
    cats = []
    [cats.append(cat["blog_category"])  for cat in categories if cat["blog_category"] not in cats ]
    cats = cats[:10]
    blogs = [] 
    for cat in cats[:6] :
        item = BlogPost.objects.filter(blog_category=cat,blog_status='p')
        if len(item) != 0 :  
            item[0].blog_content = BeautifulSoup(item[0].blog_content).get_text()[:50]
            blogs.append(item[0])

    return render(req, 'blog/index.html',{'title':'blog','categories': cats, "blogs": blogs})
def post(req,id): 
    try: 
        post = BlogPost.objects.get(blog_id=id)
        if post.blog_status == 'p':
            postedItem = {"title": post.blog_title, "date" : post.date, "content": post.blog_content, "image" : post.blog_image, "category": post.blog_category, "author": post.blog_author, "desc": BeautifulSoup(post.blog_content).get_text()}
            return render(req,'blog/post.html', postedItem)
        raise Http404("Post does not exists")
    except BlogPost.DoesNotExist:
        raise Http404("Post does not exists")
def postItem(req): 
    blogs = BlogPost.objects.filter(blog_status='p')[:10]
    for blog in blogs:
        blog.blog_content = BeautifulSoup(blog.blog_content).get_text()[:160]
        blog.date = utils.pretty_date(blog.date)
        
    return render(req, 'blog/show_blog.html', {'blogs': blogs, "length": len(blogs)})