from django.contrib import admin
from .models import Customer,Products,Cart,Order,Contact
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','address','city','state','pincode']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','category','small_description','selling_price']    

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','message']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'customer', 'product', 'quantity', 'order_at', 'status',]    