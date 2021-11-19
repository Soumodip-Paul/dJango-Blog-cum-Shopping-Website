from django.http.response import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .models import PlacedOrder, Product,Contact
from datetime import date
from math import ceil
import json


# Create your views here.
def index(req): 
    allProducts = []
    products = Product.objects.values('product_category', 'id')
    categories = { items['product_category'] for items in products }
    for category in categories : 
        product = Product.objects.filter(product_category = category)
        n = len(product)
        nSlides = n // 4 + ceil((n / 4 )- (n // 4))
        allProducts.append([product, range(1, nSlides), nSlides])
    return render(req, 'kart/index.html', {'title':'Welcome to CoMitra kart', 'allProduct' : allProducts})
def about(req): 
    return render(req, 'kart/index.html', {'title':'about'})
def search(req): 
    return render(req, 'kart/index.html', {'title':'search'})
def view(req): 
    return render(req, 'kart/index.html', {'title':'view'})
def pricing(req):
    if req.method == "POST" :
        data = json.loads(req.body.decode("utf-8"))
        prices = {}
        for id in data: 
            product = Product.objects.get(id=id)
            prices[id] = {}
            prices[id]['price'] = product.product_price
            prices[id]['name'] = product.product_name
            prices[id]['category'] = product.product_category
        return JsonResponse(prices)
    raise PermissionDenied()
def contact(req): 
    if req.method == "POST": 
        name = req.POST.get('name','')
        email = req.POST.get('email','')
        desc = req.POST.get('desc','')
        if not name=='' and not email=='' and not desc=='':
            contact = Contact(name=name,email=email,desc=desc,date=date.today())
            contact.save()
    return render(req, 'kart/contact_us.html', {'title':'Contact Us'})
def checkout(req): 
    if req.method == 'POST' : 
        name = req.POST.get('fName', '') +' '+ req.POST.get('lName')
        order = req.POST.get('itemsJson', '')
        email = req.POST.get('uEmail', '')
        phone = req.POST.get('uPhone','')
        address = req.POST.get('address1','') + ' ' + req.POST.get('address2')
        district = req.POST.get('district', '')
        state = req.POST.get('state', '')
        pin_code = req.POST.get('pin_code', '')
        if not name == '' and not order == '{}' and not email == '' and not phone == '' and not pin_code == '':
            order = PlacedOrder(name=name,email=email, items_ordered=order, phone=phone, address=address,district=district,state=state,pin_code=pin_code,date=date.today()
            )
            order.save()
            return render(req, 'kart/checkout.html', {'order_id': order.id, 'success': True})
    return render(req, 'kart/checkout.html', {'success': False})