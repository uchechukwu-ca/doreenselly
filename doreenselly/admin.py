from django.contrib import admin

from doreenselly.models import Signup, AddInventory, Cart, Order
# Register your models here.

class SignupAdmin(admin.ModelAdmin):
	list_display = ['country']

admin.site.register(Signup, SignupAdmin)

class AddInventoryAdmin(admin.ModelAdmin):
	list_display = ('client','docfile', 'description', 'price', 'shipping_weight', 'quantity', 'sold', 'item_remaining', 'total_payments', 'details')

admin.site.register(AddInventory, AddInventoryAdmin)

class CartAdmin(admin.ModelAdmin):
	list_display = ('client', 'description', 'price', 'quantity', 'ordered', 'order', 'total', 'created_on')

admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('client', 'order_number', 'location', 'payment_status', 'shipment_status', 'created_on')

admin.site.register(Order, OrderAdmin)