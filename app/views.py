from unicodedata import category
from django.shortcuts import render, redirect
from .models import Customer, Product, OrderPlaced, Cart
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator 

class ProductView(View):
    def get(self, request):
        total_item = 0
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html', {
            'mobiles':mobiles, 'laptops':laptops,
            'topwears': topwears, 'bottomwears':bottomwears,
            'total_item': total_item
        })

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        item_already_in_cart = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
        total_item = len(Cart.objects.filter(user=request.user))
    else:
        item_already_in_cart = False
        total_item = 0

    return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'total_item':total_item})

@login_required
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
        total_item = len(cart)
        if not total_item:
            return render(request, 'app/empty.html', {'total_item':total_item})
        amount = 0.0
        shipping_amount = 40.0
        total = 0.0
        for temp_cart in cart:
            amount += temp_cart.quantity*temp_cart.product.discounted_price
        total = shipping_amount + amount

        return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'shipping_amount':shipping_amount, 'total':total, 'total_item':total_item})

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 add = Customer.objects.filter(user=request.user)
 total_item = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html', {'add': add, 'total_item':total_item})

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    total_item = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'orders':op, 'total_item':total_item})

def mobile(request, data=None):
    if data is None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    else:
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    else:
        total_item = 0

    return render(request, 'app/mobile.html', {'mobiles':mobiles, 'total_item':total_item})

def laptop(request, data=None):
    if data is None:
        laptops = Product.objects.filter(category='L')
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=40000)
    else:
        laptops = Product.objects.filter(category='L').filter(brand=data)
    
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    else:
        total_item = 0

    return render(request, 'app/laptop.html', {'laptops':laptops, 'total_item':total_item})

def bottomwear(request, data=None):
    if data is None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=600)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=600)
    else:
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    else:
        total_item = 0
    return render(request, 'app/bottomwear.html', {'bottomwears':bottomwears, 'total_item':total_item})

def topwear(request, data=None):
    if data is None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=600)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=600)
    else:
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    else:
        total_item = 0

    return render(request, 'app/topwear.html', {'topwears':topwears, 'total_item':total_item})


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


@login_required
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

@login_required
def payment_done(request):
    user = request.user
    cust_id = request.GET['cust_id']
    customer = Customer.objects.get(id=cust_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        total_item = len(Cart.objects.filter(user=request.user))
        
        return render(request, 'app/profile.html', {'form':form, 'total_item':total_item})

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



        

