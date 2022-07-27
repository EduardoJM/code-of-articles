from django.contrib import admin
from products.models import Product, Purchase

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'total_purchased_value']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'purchase_final_value']
