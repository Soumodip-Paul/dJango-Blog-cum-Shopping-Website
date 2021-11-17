from django.shortcuts import render

# Create your views here.
def index(req): 
    return render(req, 'kart/index.html', {'title':'blog'})
def about(req): 
    return render(req, 'kart/index.html', {'title':'about'})
def search(req): 
    return render(req, 'kart/index.html', {'title':'search'})
def view(req): 
    return render(req, 'kart/index.html', {'title':'view'})
