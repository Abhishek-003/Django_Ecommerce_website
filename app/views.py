from unicodedata import category
from django.shortcuts import render
from .models import Customer, Product, OrderPlaced, Cart
from django.views import View

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

def product_detail(request):
 return render(request, 'app/productdetail.html')

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

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')
