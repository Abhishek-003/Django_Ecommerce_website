from django.contrib import admin
from .models import (
    Customer,
    Product, 
    Cart,
    OrderPlaced
)


class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 
                   'zipcode', 'state']


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description',
                   'brand', 'category', 'product_image']


class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status']

admin.site.register(Customer, CustomerModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Cart, CartModelAdmin)
admin.site.register(OrderPlaced, OrderPlacedModelAdmin)
    

