from unicodedata import category
from django.shortcuts import render, redirect
from .models import Customer, Product, OrderPlaced, Cart
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

class ProductView(View):
    def get(self, request):
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')

        return render(request, 'app/home.html', {
            'mobiles':mobiles, 'laptops':laptops,
            'topwears': topwears, 'bottomwears':bottomwears
        })

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'app/productdetail.html', {'product':product})

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    try:
        existing_cart = Cart.objects.get(product=product)
        existing_cart.quantity += 1
        existing_cart.save()
    except:
        Cart(user=user, product=product).save()
    return redirect("/cart")

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        if not cart:
            return render(request, 'app/empty.html')
        amount = 0.0
        shipping_amount = 40.0
        total = 0.0
        for temp_cart in cart:
            amount += temp_cart.quantity*temp_cart.product.discounted_price
        total = shipping_amount + amount

        return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'shipping_amount':shipping_amount, 'total':total})

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add': add})

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    else:
        mobiles = Product.objects.filter(category='M').filter(brand=data)

    return render(request, 'app/mobile.html', {'mobiles':mobiles})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations you are registered successfully !!!')
        return render(request, 'app/customerregistration.html', {'form':form})


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 40.0
    total = 0.0
    for temp_cart in cart:
        amount += temp_cart.quantity*temp_cart.product.discounted_price
    total = shipping_amount + amount
    return render(request, 'app/checkout.html', {'add':add, 'total':total, 'cart':cart})

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        
        return render(request, 'app/profile.html', {'form':form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            state = form.cleaned_data['state']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations!! Profile Updated Successfully")
        return render(request, 'app/profile.html', {'form':form})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        c = Cart.objects.get(Q(product=product) & Q(user=request.user))
        c.quantity += 1
        c.save()
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amount = 40.0
        total = 0.0
        for temp_cart in cart:
            amount += temp_cart.quantity*temp_cart.product.discounted_price
        total = shipping_amount + amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total': total
        }

        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        c = Cart.objects.get(Q(product=product) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amount = 40.0
        total = 0.0
        for temp_cart in cart:
            amount += temp_cart.quantity*temp_cart.product.discounted_price
        total = shipping_amount + amount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'total': total
        }

        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        c = Cart.objects.get(Q(product=product) & Q(user=request.user))
        c.delete()
        cart = Cart.objects.filter(user=request.user)
        amount = 0.0
        shipping_amount = 40.0
        total = 0.0
        for temp_cart in cart:
            amount += temp_cart.quantity*temp_cart.product.discounted_price
        total = shipping_amount + amount

        data = {
            'amount': amount,
            'total': total
        }

        return JsonResponse(data)



        

