from unicodedata import category
from django.shortcuts import render
from .models import Customer, Product, OrderPlaced, Cart
from .forms import CustomerRegistrationForm
from django.views import View
from django.contrib import messages

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
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

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
 return render(request, 'app/checkout.html')
