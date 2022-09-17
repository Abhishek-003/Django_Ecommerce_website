from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

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
    list_display = ['id', 'user', 'customer', 'customer_info', 'product', 'product_info', 'quantity', 'ordered_date', 'status']

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html("<a href='{}'>{}</a>", link, obj.customer.name)
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html("<a href='{}'>{}</a>", link, obj.product.title)

admin.site.register(Customer, CustomerModelAdmin)
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Cart, CartModelAdmin)
admin.site.register(OrderPlaced, OrderPlacedModelAdmin)
    

