from heapq import nsmallest
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.
def index(req):
    
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nSlides),nSlides])

    params = {'allProds':allProds}
    return render(req,'shop/index.html',params)

def about(req):
    return render(req,'shop/about.html')

def contact(req):
    if req.method=="POST":
        name = req.POST.get('name','')
        email = req.POST.get('email','')
        subject = req.POST.get('subject','')
        text = req.POST.get('text','')
    
        cont = Contact(name=name, email=email,subject=subject,text=text)
        cont.save()
    return render(req,'shop/contact.html')

def tracker(req):
    if req.method=="POST":
        orderId = req.POST.get('orderId'," ")
        email = req.POST.get('email'," ")

        try:
            order = Order.objects.filter(order_id=orderId,email=email)

            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []

                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates,default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        
        except:
            return HttpResponse('{}')

    return render(req,'shop/tracker.html')

def check(task,x):
    if task in x.product_name.lower() or task in x.category.lower() or task in x.subcategory.lower() or task in x.desc.lower():
        return True
    else:
        return False

def search(req):
    task = req.GET.get('search')
    allProds=[]
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        prodlist = [x for x in prod if check(task,x)]

        n=len(prodlist)

        nSlides = n//4 + ceil((n/4)-(n//4))

        if len(prodlist)!=0:
            allProds.append([prodlist,range(1,nSlides),nSlides])
        
    params = {'allProds':allProds,'flag':1}

    if len(allProds)==0:
        params={'flag':0}

    return render(req,'shop/search.html',params)

def productview(req,myid):
    product = Product.objects.filter(id=myid)
    return render(req,'shop/productview.html',{'product': product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        shopstatus = True
        update = OrderUpdate(order_id=order.order_id, update_desc="Your order placed and is at departing state")
        update.save()
        id = order.order_id

        return render(request, 'shop/checkout.html',{'shopstatus': shopstatus,'id': id})
    return render(request, 'shop/checkout.html')


