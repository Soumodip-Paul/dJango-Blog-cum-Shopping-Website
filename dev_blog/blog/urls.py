from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('search', views.search, name='blogSearch'),
    path('videos/', views.videos, name='blogVideo'),
    path('category/', views.videos, name='blogVideo'),
    path('category/<str:id>', views.category, name='blogCategory'),
    path('blogpost/', views.postItem, name='blogpost'),
    path('blogpost/<int:id>', views.post, name='blogpost')
]