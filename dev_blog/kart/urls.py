from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='kart'),
    path('about/', views.about, name='kartAbout'),
    path('contact/', views.index, name='kartContat'),
    path('traker/', views.index, name='kartTraker'),
    path('search/', views.search, name='kartSearch'),
    path('view/', views.view, name='kartView'),
    path('checkout/', views.index, name='kartCheckout'),
]