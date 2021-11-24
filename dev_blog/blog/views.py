from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import BlogPost, VideoCategory
from .utils import prettyFilter,pretty_date

# Create your views here.
def index(req):
    categories = BlogPost.objects.values('blog_category')
    cats = []
    [cats.append(cat["blog_category"])  for cat in categories if cat["blog_category"] not in cats ]
    blogs = [] 
    for cat in cats[:6] :
        item = BlogPost.objects.filter(blog_category=cat,blog_status='p')
        if len(item) != 0 :  
            item[0].blog_content = BeautifulSoup(item[0].blog_content,"html.parser").get_text()[:50]
            item[0].date = pretty_date(item[0].date)
            blogs.append(item[0])

    return render(req, 'blog/index.html',{'title':'blog','categories': cats, "blogs": blogs})
def post(req,id): 
    try: 
        post = BlogPost.objects.get(blog_id=id)
        if post.blog_status == 'p':
            postedItem = {"title": post.blog_title, "date" : post.date, "content": post.blog_content, "image" : post.blog_image, "category": post.blog_category, "author": post.blog_author, "desc": BeautifulSoup(post.blog_content, "html.parser").get_text()}
            return render(req,'blog/post.html', postedItem)
        raise Http404("Post does not exists")
    except BlogPost.DoesNotExist:
        raise Http404("Post does not exists")
def postItem(req): 
    blogs = BlogPost.objects.filter(blog_status='p')[:10]        
    return render(req, 'blog/show_blog.html', {'blogs': prettyFilter(blogs)})

def search(req):
    qString = req.GET.get('q')
    results = []
    if qString != None and len(qString) != 0:
        result = BlogPost.objects.filter(blog_title__icontains=qString)
        results = [ item  for item in result]
        result = BlogPost.objects.filter(blog_content__icontains=qString)
        results.extend([item for item in result if item not in results])
        results = results[:10]
    return render(req, 'blog/search.html', {'qs': qString or '' , 'results': prettyFilter(results) })

def videos(req):
    items = VideoCategory.objects.all()
    video_category = [item for item in items]
    print(video_category)
    return render(req,'blog/video_categories.html', {'categories': video_category})
def category(req,id):
    items = BlogPost.objects.filter(blog_category=id,blog_status='p')
    blogs = []
    if items != None:
        blogs = [ item for item in items[:10] ]
    return render(req, 'blog/show_blog.html', {'blogs': prettyFilter(blogs), 'category': id })