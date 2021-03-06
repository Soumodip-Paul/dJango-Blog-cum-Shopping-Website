from django.urls import path

from . import payments
from . import views

urlpatterns = [
    path('', views.index, name='kart'),
    path('about/', views.about, name='kartAbout'),
    path('contact/', views.contact, name='kartContact'),
    path('track/', views.index, name='kartTraker'),
    path('search/', views.search, name='kartSearch'),
    path('view/', views.view, name='kartView'),
    path('checkout/', payments.startPayment, name='kartCheckout'),
    path('faqs/', views.index, name='kartFaqs'),
    path('price/', views.pricing, name="kartPricing"),
    path('payment/', payments.validate, name="kartPayment")
]