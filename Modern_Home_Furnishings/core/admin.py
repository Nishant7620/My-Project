from django.contrib import admin
from .models import Customer,Products,Cart
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','address','city','state','pincode']

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','category','small_description','selling_price']    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']