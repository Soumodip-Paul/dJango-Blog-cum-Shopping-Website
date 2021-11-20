from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blog'),
    path('blogpost/', views.postItem, name='blogpost'),
    path('blogpost/<int:id>', views.post, name='blogpost')
]