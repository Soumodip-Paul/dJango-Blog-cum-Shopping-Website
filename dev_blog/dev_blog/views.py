# This is created by - Soumodip Paul

from django.http import HttpResponse
from django.shortcuts import render

def index(request): 
    print(request.GET.get('text', 'default'))
    params = {'title': 'Django Learning'}
    return render(request, 'index.html', params)

def about(request): 
    return HttpResponse("About page")