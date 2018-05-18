from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(req):
    # Product.objects.all().delete()
    # Sales.objects.all().delete()
    return render(req, 'myapp/index.html')


def register(req):

    results = User.objects.regValidator(req.POST)
    print(results)

    if results[0]:
        req.session['id'] = results[1].id
        req.session['name'] = results[1].fname
        return redirect('/dashboard')
    else:

        for error in results[1]:
            messages.add_message(req, messages.ERROR, error, extra_tags='register')

        return redirect('/')


def dashboard(req, user_id=None):


    context = {
        "products_not_sold" : Product.objects.filter(isSold=False, seller_id = req.session['id']),
        # "products_sold" : Product.objects.filter(isSold=True, seller_id=req.session['id']).select_related("seller"),
        "products_sold" : Sales.objects.all().select_related("product", "buyer").filter(product__isSold=True, product__seller_id=req.session['id']),
        "purchases" : Sales.objects.filter(buyer_id=req.session['id']).select_related("product__seller", "buyer")
    }

    return render(req, 'myapp/dashboard.html', context)


def login(req):

    results = User.objects.loginValidator(req.POST)
    print(results)

    if results[0]:
        req.session['id'] = results[1].id
        req.session['name'] = results[1].fname

        # return redirect('/dashboard')
        return redirect('/dashboard/{}'.format(req.session['id']))
    else:
        for error in results[1]:
            messages.add_message(req, messages.ERROR, error, extra_tags='login')
        return redirect('/')

def sell(req):

    results = Product.objects.productValidator(req.POST, req.session['id'])
    # print(results)
    return redirect('/dashboard/{}'.format(req.session['id']))

def shoes(req):
    context = {
        "all_products_for_sale" : Product.objects.filter(isSold=False)
    }

    return render(req, 'myapp/shoes.html', context)

def buy(req, id):

    product = Product.objects.get(id=id)
    product.isSold=True
    product.save()
    Sales.objects.create(product_id=id, buyer_id=req.session['id'])
    return redirect('/shoes')
